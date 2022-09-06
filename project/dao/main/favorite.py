from flask_sqlalchemy import SQLAlchemy
from project.models import UserMovie


class FavoriteDAO:

    def __init__(self, session: SQLAlchemy().session):
        self.session = session

    def create(self, data: dict) -> UserMovie | bool:
        item = UserMovie(**data)
        try:
            self.session.add(item)
            self.session.commit()
        except Exception:
            return False

        return item

    def delete(self, data: dict) -> bool:
        try:
            self.session.query(UserMovie).filter(
                UserMovie.movie_id == data.get("movie_id"),
                UserMovie.user_id == data.get("user_id")
            ).delete()
            self.session.commit()
        except Exception:
            return False

        return True
