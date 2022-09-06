from flask import request, current_app as app, url_for
from flask_restx import Resource, Namespace

from project.container import movie_service
from project.models import MovieSchema
from project.setup.api.models import movie_api_model, error_api_model
from project.setup.api.parsers import movie_state_filter_and_page_parser

api: Namespace = Namespace("movies")

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


@api.route("/")
class MoviesView(Resource):
    """Shows a list of all movies, and lets you POST to add new movies"""

    @api.expect(movie_state_filter_and_page_parser)  # <- from Frontend
    @api.marshal_list_with(movie_api_model, code=200, description='OK')  # -> to Frontend
    def get(self):
        """List all movies"""

        movies = movie_service.get_all(movie_state_filter_and_page_parser.parse_args(),
                                       app.config.get("ITEMS_PER_PAGE"))
        return movies_schema.dump(movies), 200

    @api.expect(movie_api_model)
    @api.response(201, description="OK", model=movie_api_model,
                  headers={'Location': 'The URL of a newly created movie'})
    @api.response(404, description="Not Found", model=error_api_model)
    def post(self):
        """Create a new movie"""

        try:
            movie: dict = movie_schema.load(request.json)
            response = movie_service.create(movie)
        except Exception:
            return None, 400
        else:
            return movie_schema.dump(response), 201, {'Location': url_for('movies_movie_view', mid=response.id)}


@api.route("/<int:mid>")
class MovieView(Resource):
    """Show a single movie item and lets you delete them"""

    # @movies_ns.expect(page_parser)
    @api.marshal_with(movie_api_model, code=200, description='OK')
    @api.response(404, description="Not Found", model=error_api_model)
    def get(self, mid: int):
        """Fetch a given resource"""

        movie = movie_service.get_by_id(mid)
        return movie_schema.dump(movie), 200

    @api.expect(movie_api_model)
    @api.response(204, description="No Content")
    @api.response(404, description="Not Found", model=error_api_model)
    def put(self, mid: int):
        """Update a movie given its identifier"""

        data: dict = request.json
        data['id'] = mid
        if movie_service.update(data):
            return None, 204
        return None, 404

    @api.response(204, description="No Content")
    @api.response(404, description="Not Found")
    def delete(self, mid: int):
        """Delete a movie given its identifier"""

        if movie_service.delete(mid):
            return None, 204
        return None, 404
