from flask import current_app as app
from flask_restx import Namespace, Resource

from project.container import genre_service
from project.setup.api.models import genre_api_model, error_api_model
from project.setup.api.parsers import page_parser

api = Namespace('genres')


@api.route('/')
class GenresView(Resource):
    @api.expect(page_parser)
    @api.marshal_list_with(genre_api_model, code=200, description='OK')
    def get(self):
        """Get all genres"""

        return genre_service.get_all(page_parser.parse_args(), app.config.get("ITEMS_PER_PAGE"))


@api.route('/<int:genre_id>/')
class GenreView(Resource):
    @api.marshal_with(genre_api_model, code=200, description='OK')
    @api.response(404, 'Not Found', model=error_api_model)
    def get(self, genre_id: int):
        """Get genre by id"""

        return genre_service.get_by_id(genre_id)
