from project.dao.main.movie import MovieDAO


class MovieService:

    def __init__(self, dao: MovieDAO):
        self._dao = dao

    def create(self, data: dict):
        return self._dao.create(data)

    def get_all(self, args: dict, per_page: int):
        page = args.get('page')
        status = args.get('status')
        fields = {k: v for k, v in args.items() if k not in ['page', 'status'] if v}

        return self._dao.get_all(page, per_page, fields, status)

    def get_by_id(self, mid: int):
        return self._dao.get_by_id(mid)

    def update(self, data: dict) -> bool:
        return self._dao.update(data)

    def delete(self, mid: int) -> bool:
        return self._dao.delete(mid)
