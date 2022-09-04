from flask import request, abort
import jwt
from jwt import PyJWTError
import logging

from project.helpers.constants import JWT_SECRET, JWT_ALGORITHM


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        token = request.headers['Authorization'].split("Bearer ")[-1]
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except PyJWTError as e:
            logging.warning(e)
            abort(401)
        except Exception as e:
            logging.warning(e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        token = request.headers['Authorization'].split("Bearer ")[-1]
        role = None
        try:
            user: dict = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get('role', 'user')
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        if role != 'admin':
            abort(403)
        return func(*args, **kwargs)

    return wrapper


if __name__ == "__main__":
    pass
