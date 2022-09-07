import base64
import hashlib

from project.config import config


class RegService:

    def generate_password(self, password: str) -> str:
        hash_digest = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=config.PWD_HASH_SALT,
            iterations=config.PWD_HASH_ITERATIONS,
        )

        return base64.b64encode(hash_digest).decode('utf-8')
