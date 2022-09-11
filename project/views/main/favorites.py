from flask import request
from flask_restx import Resource, Namespace

from project.container import favorite_service, auth_service
from project.helpers.decorators import auth_required
from project.models import UserMovieSchema
from project.setup.api.models import error_api_model, favorite_api_model


api: Namespace = Namespace("favorite")

favorite_schema = UserMovieSchema()


@api.route("/movies/<int:movie_id>")
class FavoriteEdit(Resource):
    """Edit favorites"""

    @api.marshal_with(favorite_api_model, code=201, description='OK')
    @api.response(401, description="Unauthorized", model=error_api_model)
    @api.response(404, description="Not Found", model=error_api_model)
    @auth_required
    def post(self, movie_id: int):
        """Add a movie to favorites"""

        email: str = auth_service.decode_token(request.headers['Authorization']).get('email')
        data = {"email": email, "movie_id": movie_id}
        response = favorite_service.create(data)
        if not response:
            return None, 400

        return favorite_schema.dump(response), 201

    @api.response(204, description="No Content")
    @api.response(401, description="Unauthorized", model=error_api_model)
    @api.response(404, description="Not Found", model=error_api_model)
    @auth_required
    def delete(self, movie_id: int):
        """Delete a movie from favorites"""

        email: str = auth_service.decode_token(request.headers['Authorization']).get('email')
        data = {"email": email, "movie_id": movie_id}

        if favorite_service.delete(data):
            return None, 204

        return None, 404
