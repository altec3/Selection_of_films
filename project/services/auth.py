from project.helpers.constants import JWT_SECRET, JWT_ALGORITHM, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from flask import abort
import base64
import calendar
import datetime
import hashlib
import hmac
import jwt

from project.services.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self._user_service = user_service
        self._jwt_secret = JWT_SECRET
        self._jwt_algorithm = JWT_ALGORITHM
        self._pwd_salt = PWD_HASH_SALT
        self._pwd_iterations = PWD_HASH_ITERATIONS

    def generate_tokens(self, auth_data: dict, is_refresh: bool = False) -> dict:
        email = auth_data.get("email", None)
        password = auth_data.get("password", None)

        user = self._user_service.get_by_email(email)

        if not is_refresh:
            if not self.compare_passwords(user.password, password):
                abort(400)

        data = {
            "email": user.email,
            "role": user.role,
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, self._jwt_secret, algorithm=self._jwt_algorithm)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, self._jwt_secret, algorithm=self._jwt_algorithm)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def decode_token(self, data: str) -> dict:
        token: str = data.split("Bearer ")[-1]
        return jwt.decode(token, self._jwt_secret, algorithms=[self._jwt_algorithm])

    def approve_refresh_token(self, auth_data: dict):
        refresh_token = auth_data.get("refresh_token")
        data: dict = jwt.decode(jwt=refresh_token, key=self._jwt_secret, algorithms=[self._jwt_algorithm])

        return self.generate_tokens(data, is_refresh=True)

    def compare_passwords(self, password_hash: bytes, other_password: str) -> bool:
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac(
                hash_name="sha256",
                password=other_password.encode("utf-8"),
                salt=self._pwd_salt,
                iterations=self._pwd_iterations,
            )
        )
