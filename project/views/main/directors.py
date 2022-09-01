from flask import current_app as app
from flask_restx import Namespace, Resource

from project.container import director_service
from project.setup.api.models import director_api_model
from project.setup.api.parsers import page_parser

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    @directors_ns.expect(page_parser)
    @directors_ns.marshal_with(director_api_model, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all genres.
        """
        return director_service.get_all(page_parser.parse_args(), app.config.get("ITEMS_PER_PAGE"))


@directors_ns.route('/<int:genre_id>/')
class DirectorView(Resource):
    @directors_ns.response(404, 'Not Found')
    @directors_ns.marshal_with(director_api_model, code=200, description='OK')
    def get(self, genre_id: int):
        """
        Get genre by id.
        """
        return director_service.get_item(genre_id)
