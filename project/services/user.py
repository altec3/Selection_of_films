from project.dao.main.user import UserDAO
from project.services.reg import RegService


class UserService:

    def __init__(self, dao: UserDAO, reg: RegService):
        self._dao = dao
        self.reg = reg

    def create(self, data: dict):
        data["password"] = self.reg.generate_password(data.get("password"))
        return self._dao.create(data)

    def get_all(self, page: int, per_page: int):
        return self._dao.get_all(page, per_page)

    def get_by_id(self, uid: int):
        return self._dao.get_by_id(uid)

    def get_by_email(self, email: str):
        return self._dao.get_by_email(email)

    def update(self, data: dict) -> bool:
        return self._dao.update(data)

    def delete(self, uid: int) -> bool:
        return self._dao.delete(uid)

    def change_password(self, data: dict) -> bool:
        user = self.get_by_email(data.get("email"))
        new_password = self.reg.generate_password(data.get("new_password"))

        if user.password != new_password:
            data = {
                "email": user.email,
                "password": new_password
            }
            return self._dao.update(data)

        return False
