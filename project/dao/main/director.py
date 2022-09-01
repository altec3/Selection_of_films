from project.models import Director

from flask_sqlalchemy import SQLAlchemy


class DirectorDAO:

    def __init__(self, session: SQLAlchemy().session):
        self.session = session

    def create(self, data: dict) -> Director:
        director = Director(**data)
        self.session.add(director)
        self.session.commit()

        return director

    def get_all(self, page: int, per_page: int) -> list[Director]:
        if page:
            return self.session.query(Director).paginate(page, per_page, False).items

        return self.session.query(Director).all()

    def get_by_id(self, did: int) -> Director:
        return self.session.query(Director).get_or_404(did)

    def update(self, data: dict) -> bool:
        did = data.get('id')
        if self.session.query(Director).filter(Director.id == did).update(data):
            self.session.commit()
            return True

        return False

    def delete(self, did: int) -> bool:
        if self.session.query(Director).filter(Director.id == did).delete():
            self.session.commit()
            return True

        return False
