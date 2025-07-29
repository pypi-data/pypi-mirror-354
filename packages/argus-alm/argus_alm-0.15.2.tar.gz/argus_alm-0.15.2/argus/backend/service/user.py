from datetime import datetime
import functools
import hashlib
import os
import base64
from uuid import UUID
from time import time
from hashlib import sha384

from flask import current_app, flash, g, redirect, request, session, url_for
import requests
from werkzeug.security import generate_password_hash, check_password_hash

from argus.backend.db import ScyllaCluster
from argus.backend.error_handlers import APIException
from argus.backend.models.web import User, UserOauthToken, UserRoles, WebFileStorage
from argus.backend.util.common import FlaskView


class UserServiceException(Exception):
    pass


class GithubOrganizationMissingError(Exception):
    pass


class UserService:
    def __init__(self) -> None:
        self.cluster = ScyllaCluster.get()
        self.session = self.cluster.session

    @staticmethod
    def check_roles(roles: list[UserRoles] | UserRoles, user: User) -> bool:
        if not user:
            return False
        if isinstance(roles, str):
            return roles in user.roles
        elif isinstance(roles, list):
            for role in roles:
                if role in user.roles:
                    return True
        return False

    def github_callback(self, req_code: str) -> dict | None:
        if "gh" not in current_app.config.get("LOGIN_METHODS", []):
            raise UserServiceException("Github Login is disabled")
        oauth_response = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={
                "Accept": "application/json",
            },
            params={
                "code": req_code,
                "client_id": current_app.config.get("GITHUB_CLIENT_ID"),
                "client_secret": current_app.config.get("GITHUB_CLIENT_SECRET"),
            }
        )

        oauth_data = oauth_response.json()

        user_info = requests.get(
            "https://api.github.com/user",
            headers={
                "Accept": "application/json",
                "Authorization": f"token {oauth_data.get('access_token')}"
            }
        ).json()
        email_info = requests.get(
            "https://api.github.com/user/emails",
            headers={
                "Accept": "application/json",
                "Authorization": f"token {oauth_data.get('access_token')}"
            }
        ).json()

        organizations = requests.get(
            "https://api.github.com/user/orgs",
            headers={
                "Accept": "application/json",
                "Authorization": f"token {oauth_data.get('access_token')}"
            }
        ).json()

        temp_password = None
        required_organizations = current_app.config.get("GITHUB_REQUIRED_ORGANIZATIONS")
        if required_organizations:
            logins = set([org["login"] for org in organizations])
            required_organizations = set(required_organizations)
            if len(logins.intersection(required_organizations)) == 0:
                raise GithubOrganizationMissingError(
                    "Not a member of a required organization or missing organization scope")

        try:
            user = User.get(username=user_info.get("login"))
        except User.DoesNotExist:
            user = User()
            user.username = user_info.get("login")
            # pick only scylladb.com emails
            scylla_email = next(iter([email.get("email")
                                for email in email_info if email.get("email").endswith("@scylladb.com")]), None)
            primary_email = next(iter([email.get("email")
                                 for email in email_info if email.get("primary") and email.get("verified")]), None)
            user.email = scylla_email or primary_email
            user.full_name = user_info.get("name", user_info.get("login"))
            user.registration_date = datetime.utcnow()
            user.roles = ["ROLE_USER"]
            temp_password = base64.encodebytes(
                os.urandom(48)).decode("ascii").strip()
            user.password = generate_password_hash(temp_password)

            avatar_url: str = user_info.get("avatar_url")
            avatar = requests.get(avatar_url).content
            avatar_name = avatar_url.split("/")[-1]
            filename, filepath = self.save_profile_picture_to_disk(avatar_name, avatar, user.username)

            web_file = WebFileStorage()
            web_file.filename = filename
            web_file.filepath = filepath
            web_file.save()
            user.picture_id = web_file.id
            user.save()

        try:
            tokens = list(UserOauthToken.filter(user_id=user.id).all())
            github_token = [
                token for token in tokens if token["kind"] == "github"][0]
            github_token.token = oauth_data.get('access_token')
            github_token.save()
        except (UserOauthToken.DoesNotExist, IndexError):
            github_token = UserOauthToken()
            github_token.kind = "github"
            github_token.user_id = user.id
            github_token.token = oauth_data.get('access_token')
            github_token.save()

        redirect_target = session.get("redirect_target")
        session.clear()
        session["user_id"] = str(user.id)
        session["redirect_target"] = redirect_target
        if temp_password:
            return {
                "password": temp_password,
                "first_login": True
            }
        return None

    def get_users(self) -> dict:
        users = User.all()
        return {str(user.id): user.to_json() for user in users}

    def get_users_privileged(self) -> dict:
        users = User.all()
        users = {str(user.id): dict(user.items()) for user in users}
        for user in users.values():
            user.pop("password")
            user.pop("api_token")

        return users

    def generate_token(self, user: User):
        token_digest = f"{user.username}-{int(time())}-{base64.encodebytes(os.urandom(128)).decode(encoding='utf-8')}"
        new_token = base64.encodebytes(sha384(token_digest.encode(encoding="utf-8")
                                              ).digest()).decode(encoding="utf-8").strip()
        user.api_token = new_token
        user.save()
        return new_token

    def update_email(self, user: User, new_email: str):
        user.email = new_email
        user.save()

        return True

    def toggle_admin(self, user_id: str):
        user: User = User.get(id=user_id)

        if user.id == g.user.id:
            raise UserServiceException("Cannot toggle admin role from yourself.")

        is_admin = UserService.check_roles(UserRoles.Admin, user)

        if is_admin:
            user.roles.remove(UserRoles.Admin)
        else:
            user.set_as_admin()

        user.save()
        return True

    def delete_user(self, user_id: str):
        user: User = User.get(id=user_id)
        if user.id == g.user.id:
            raise UserServiceException("Cannot delete user that you are logged in as.")

        if user.is_admin():
            raise UserServiceException("Cannot delete admin users. Unset admin flag before deleting")

        user.delete()

        return True

    def update_password(self, user: User, old_password: str, new_password: str, force=False):
        if not check_password_hash(user.password, old_password) and not force:
            raise UserServiceException("Incorrect old password")

        if not new_password:
            raise UserServiceException("Empty new password")

        if len(new_password) < 5:
            raise UserServiceException("New password is too short")

        user.password = generate_password_hash(new_password)
        user.save()

        return True

    def update_name(self, user: User, new_name: str):
        user.full_name = new_name
        user.save()

    def save_profile_picture_to_disk(self, original_filename: str, filedata: bytes, suffix: str):
        filename_fragment = hashlib.sha256(os.urandom(64)).hexdigest()[:10]
        filename = f"profile_{suffix}_{filename_fragment}"
        filepath = f"storage/profile_pictures/{filename}"
        with open(filepath, "wb") as file:
            file.write(filedata)

        return original_filename, filepath

    def update_profile_picture(self, filename: str, filepath: str):
        web_file = WebFileStorage()
        web_file.filename = filename
        web_file.filepath = filepath
        web_file.save()

        try:
            if old_picture_id := g.user.picture_id:
                old_file = WebFileStorage.get(id=old_picture_id)
                os.unlink(old_file.filepath)
                old_file.delete()
        except Exception as exc:
            print(exc)

        g.user.picture_id = web_file.id
        g.user.save()


def login_required(view: FlaskView):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None and not getattr(view, "api_view", False):
            flash(message='Unauthorized, please login', category='error')
            session["redirect_target"] = request.full_path
            return redirect(url_for('auth.login'))
        elif g.user is None and getattr(view, "api_view", True):
            return {
                "status": "error",
                "message": "Authorization required"
            }, 403

        return view(*args, **kwargs)

    return wrapped_view


def api_login_required(view: FlaskView):
    view.api_view = True
    return login_required(view)


def check_roles(needed_roles: list[str] | str = None):
    def inner(view: FlaskView):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if not UserService.check_roles(needed_roles, g.user):
                flash(message='Not authorized to access this area', category='error')
                return redirect(url_for('main.home'))

            return view(*args, **kwargs)

        return wrapped_view
    return inner


def load_logged_in_user():
    user_id = session.get('user_id')
    auth_header = request.headers.get("Authorization")

    if user_id:
        try:
            g.user = User.get(id=UUID(user_id))
            return
        except User.DoesNotExist:
            session.clear()

    if auth_header:
        try:
            auth_schema, *auth_data = auth_header.split()
            if auth_schema == "token":
                token = auth_data[0]
                g.user = User.get(api_token=token)
                return
        except IndexError as exception:
            raise APIException("Malformed authorization header") from exception
        except User.DoesNotExist as exception:
            raise APIException("User not found for supplied token") from exception
    g.user = None
