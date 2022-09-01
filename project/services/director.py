from project.dao.main.director import DirectorDAO


class DirectorService:

    def __init__(self, dao: DirectorDAO):
        self._dao = dao

    def create(self, data: dict):
        return self._dao.create(data)

    def get_all(self, args: dict, per_page: int):
        page = args.get('page')
        return self._dao.get_all(page, per_page)

    def get_by_id(self, did: int):
        return self._dao.get_by_id(did)

    def update(self, data: dict) -> bool:
        return self._dao.update(data)

    def delete(self, did: int) -> bool:
        return self._dao.delete(did)
