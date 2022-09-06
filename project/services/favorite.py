from project.dao.main.favorite import FavoriteDAO
from project.services.user import UserService


class FavoriteService:

    def __init__(self, dao: FavoriteDAO, user_service: UserService):
        self._dao = dao
        self._user_service = user_service

    def __prepare_data(self, data: dict):
        user = self._user_service.get_by_email(data.get("email"))
        data = {
            "user_id": user.id,
            "movie_id": int(data.get("movie_id"))
        }
        return data

    def create(self, data: dict):
        return self._dao.create(self.__prepare_data(data))

    def delete(self, data: dict) -> bool:
        return self._dao.delete(self.__prepare_data(data))
