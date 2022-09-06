from flask import current_app as app
from flask_restx import Namespace, Resource

from project.container import director_service
from project.setup.api.models import director_api_model
from project.setup.api.parsers import page_parser

api = Namespace('directors')


@api.route('/')
class DirectorsView(Resource):
    @api.expect(page_parser)
    @api.marshal_list_with(director_api_model, code=200, description='OK')
    def get(self):
        """Get all directors"""

        return director_service.get_all(page_parser.parse_args(), app.config.get("ITEMS_PER_PAGE"))


@api.route('/<int:genre_id>/')
class DirectorView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(director_api_model, code=200, description='OK')
    def get(self, genre_id: int):
        """Get director by id."""

        return director_service.get_item(genre_id)
