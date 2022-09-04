import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from project.models import User


class UserDAO:

    def __init__(self, session: SQLAlchemy().session):
        self._session = session

    def create(self, data: dict):
        user = User(**data)
        try:
            self._session.add(user)
            self._session.commit()
        except Exception:
            return False
        else:
            return user

    def get_all(self, page: int, per_page: int) -> list[User]:
        return self._session.query(User).paginate(page, per_page, False).items

    def get_by_id(self, uid: int) -> User:
        return self._session.query(User).get_or_404(uid)

    def get_by_email(self, email: str) -> User:
        return self._session.query(User).filter(User.email == email).first_or_404()

    def update(self, data: dict) -> bool:
        uid = data.get('id')
        if self._session.query(User).filter(User.id == uid).update(data):
            self._session.commit()
            return True

        return False

    def delete(self, uid: int) -> bool:
        if self._session.query(User).filter(User.id == uid).delete():
            self._session.commit()
            return True

        return False


if __name__ == "__main__":
    pass
