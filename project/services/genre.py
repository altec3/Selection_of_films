from project.dao.main.genre import GenreDAO


class GenreService:

    def __init__(self, dao: GenreDAO):
        self._dao = dao

    def create(self, data: dict):
        return self._dao.create(data)

    def get_all(self, args: dict, per_page: int):
        page = args.get('page')
        return self._dao.get_all(page, per_page)

    def get_by_id(self, gid: int):
        return self._dao.get_by_id(gid)

    def update(self, data: dict) -> bool:
        return self._dao.update(data)

    def delete(self, gid: int) -> bool:
        return self._dao.delete(gid)
