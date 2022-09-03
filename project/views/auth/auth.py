from flask import url_for
from flask_restx import Namespace, Resource

from project.container import auth_service, user_service
from project.models import UserSchema
from project.setup.api.models import tokens_api_model, error_api_model, user_api_model
from project.setup.api.parsers import auth_parser, refresh_auth_parser

api = Namespace('auth')

user_schema = UserSchema()


@api.route("/register")
class RegisterView(Resource):

    @api.expect(auth_parser)  # <-- from Frontend
    @api.response(201, description="OK", model=user_api_model,
                  headers={'Location': 'The URL of a newly created user'})
    @api.response(404, description="No Found", model=error_api_model)
    @api.marshal_list_with(user_api_model, code=201, description='OK')  # --> to Frontend
    def post(self):
        """Register a new user"""

        try:
            response = user_service.create(auth_parser.parse_args())
        except Exception:
            return None, 400
        else:
            return user_schema.dump(response), 201, {'Location': url_for('movies_movie_view', mid=response.id)}


@api.route("/login")
class AuthsView(Resource):

    @api.expect(auth_parser)
    @api.marshal_list_with(tokens_api_model, code=201, description='OK')
    @api.response(400, description="Bad Request", model=error_api_model)
    @api.response(404, description="No Found", model=error_api_model)
    def post(self):
        """User authentication"""

        return auth_service.generate_tokens(auth_parser.parse_args()), 201

    @api.expect(refresh_auth_parser)
    @api.marshal_list_with(tokens_api_model, code=201, description='OK')
    @api.response(400, description="Bad Request", model=error_api_model)
    def put(self):
        """Update user authentication"""

        return auth_service.approve_refresh_token(refresh_auth_parser.parse_args()), 201
