from typing import List
from flask_sqlalchemy import SQLAlchemy

from project.models import Genre


class GenreDAO:

    def __init__(self, session: SQLAlchemy().session):
        self.session = session

    def create(self, data: dict) -> Genre:
        genre = Genre(**data)
        self.session.add(genre)
        self.session.commit()

        return genre

    def get_all(self, page: int = None, per_page: int = None) -> List[Genre]:
        if page:
            return self.session.query(Genre).paginate(page, per_page, False).items

        return self.session.query(Genre).all()

    def get_by_id(self, gid: int) -> Genre:
        return self.session.query(Genre).get_or_404(gid)

    def update(self, data: dict) -> bool:
        gid = data.get('id')
        if self.session.query(Genre).filter(Genre.id == gid).update(data):
            self.session.commit()
            return True

        return False

    def delete(self, gid: int) -> bool:
        if self.session.query(Genre).filter(Genre.id == gid).delete():
            self.session.commit()
            return True

        return False
