from project.dao.main.favorite import FavoriteDAO
from project.dao.main.user import UserDAO
from project.services.security.auth import AuthService
from project.services.favorite import FavoriteService
from project.services.security.reg import RegService
from project.services.user import UserService
from project.setup.db import db
from project.dao.main.director import DirectorDAO
from project.dao.main.genre import GenreDAO
from project.dao.main.movie import MovieDAO
from project.services.director import DirectorService
from project.services.genre import GenreService
from project.services.movie import MovieService


director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)

genre_dao = GenreDAO(db.session)
genre_service = GenreService(genre_dao)

movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)

user_dao = UserDAO(db.session)
reg_service = RegService()
user_service = UserService(user_dao, reg_service)

auth_service = AuthService(user_service)

favorite_dao = FavoriteDAO(db.session)
favorite_service = FavoriteService(favorite_dao, user_service)
