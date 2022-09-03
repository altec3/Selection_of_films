import base64
import os

JWT_SECRET = os.getenv('SECRET_KEY', 'you-will-never-guess')
JWT_ALGORITHM = 'HS256'

PWD_HASH_SALT = base64.b64decode("salt")
PWD_HASH_ITERATIONS = 100_000
