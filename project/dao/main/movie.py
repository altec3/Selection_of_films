from typing import List
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import desc

from project.models import Movie


class MovieDAO:

    def __init__(self, session: SQLAlchemy().session):
        self._session = session

    def create(self, data: dict) -> Movie:
        movie = Movie(**data)
        self._session.add(movie)
        self._session.commit()

        return movie

    def get_all(self, page: int, per_page: int, fields: dict, new: str) -> List[Movie]:
        db_query: BaseQuery = self._session.query(Movie)

        if fields:
            db_query: BaseQuery = db_query.filter_by(**fields)
        if new == 'new':
            db_query: BaseQuery = db_query.order_by(desc(Movie.year))
        if page:
            return db_query.paginate(page, per_page, False).items

        return db_query.all()

    def get_by_id(self, did: int) -> Movie:
        return self._session.query(Movie).get_or_404(did)

    def update(self, data: dict) -> bool:
        mid = data.get('id')
        if self._session.query(Movie).filter(Movie.id == mid).update(data):
            self._session.commit()
            return True

        return False

    def delete(self, mid: int) -> bool:
        if self._session.query(Movie).filter(Movie.id == mid).delete():
            self._session.commit()
            return True

        return False
