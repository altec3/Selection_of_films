from marshmallow import Schema, fields, validate

from project.setup.db import models, db


# Models for SQLAlchemy and Marshmallow
class Director(models.Base):
    __tablename__ = 'director'

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Director {self.name}>'


class DirectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=100))


class Genre(models.Base):
    __tablename__ = 'genre'

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Genre {self.name}>'


class GenreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=100))


class Movie(models.Base):
    __tablename__ = 'movie'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    trailer = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey(f"{Genre.__tablename__}.id"), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey(f"{Director.__tablename__}.id"), nullable=False)

    genre = db.relationship("Genre")
    director = db.relationship("Director")

    def __repr__(self):
        return f'<Movie {self.title}>'


class MovieSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=255))
    description = fields.String(required=True, validate=validate.Length(max=1000))
    trailer = fields.String(required=True, validate=validate.Length(max=255))
    year = fields.Integer(required=True)
    rating = fields.Integer(required=True)
    genre_id = fields.Integer(required=True)
    director_id = fields.Integer(required=True)

    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)


class User(models.Base):
    __tablename__ = 'user'

    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    role = db.Column(db.String(50), default="user")
    favorite_genre_id = db.Column(db.Integer, db.ForeignKey(f"{Genre.__tablename__}.id"))

    favorite_genre = db.relationship("Genre")

    def __repr__(self):
        return f'<User {self.email}>'


class UserSchema(Schema):

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    name = fields.String(validate=validate.Length(max=100))
    surname = fields.String(validate=validate.Length(max=100))
    role = fields.String()
    favorite_genre_id = fields.Integer()

    favorite_genre = fields.Nested(GenreSchema)


class UserMovie(db.Model):
    __tablename__ = 'user_movie'

    user_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey(f"{Movie.__tablename__}.id"))
    db.PrimaryKeyConstraint(user_id, movie_id)


class UserMovieSchema(Schema):

    user_id = fields.Integer()
    movie_id = fields.Integer()

    user = fields.Nested(UserSchema)
    movie = fields.Nested(MovieSchema)
