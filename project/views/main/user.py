from flask import request
from flask_restx import Resource, Namespace

from project.container import user_service, auth_service
from project.models import UserSchema
from project.setup.api.parsers import change_user_info_parser, change_password_parser
from project.setup.api.models import user_api_model, error_api_model
from project.helpers.decorators import auth_required

api: Namespace = Namespace('user')

user_schema = UserSchema()


@api.route("/")
class UserView(Resource):
    """Show or edit a user profile"""

    @api.marshal_with(user_api_model, code=200, description='OK')
    @api.response(401, description="Unauthorized", model=error_api_model)
    @api.response(404, description="Not Found", model=error_api_model)
    @auth_required
    def get(self):
        """Show a user profile"""

        email: str = auth_service.decode_token(request.headers['Authorization']).get('email')
        user = user_service.get_by_email(email)
        return user_schema.dump(user), 200

    @api.expect(change_user_info_parser)
    @api.response(204, description="No Content")
    @api.response(401, description="Unauthorized", model=error_api_model)
    @api.response(400, description="Bad Request", model=error_api_model)
    @auth_required
    def patch(self):
        """Edit a user profile"""

        email: str = auth_service.decode_token(request.headers['Authorization']).get('email')
        data: dict = change_user_info_parser.parse_args()
        data['email'] = email
        if user_service.update(data):
            return None, 204

        return None, 400


@api.route("/password")
class PasswordUpdate(Resource):

    @api.expect(change_password_parser)
    @api.response(204, description="No Content")
    @api.response(401, description="Unauthorized", model=error_api_model)
    @api.response(400, description="Bad Request", model=error_api_model)
    @auth_required
    def put(self):
        """Change a user password"""

        email: str = auth_service.decode_token(request.headers['Authorization']).get('email')
        data: dict = change_password_parser.parse_args()
        data['email'] = email
        if user_service.change_password(data):
            return None, 204

        return None, 400


if __name__ == "__main__":
    pass
