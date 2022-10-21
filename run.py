from project.config import config
from project.models import Director, Genre, Movie, User
from project.server import create_app, db

app = create_app(config)


# @app.shell_context_processor
# def shell():
#     return {
#         "db": db,
#         "Director": Director,
#         "Genre": Genre,
#         "Movie": Movie,
#         "User": User,
#     }
