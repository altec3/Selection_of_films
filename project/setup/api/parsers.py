from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser

auth_parser: RequestParser = RequestParser()
auth_parser.add_argument(name='email', type=email(), location='json', required=True, nullable=False)
auth_parser.add_argument(name='password', type=str, location='json', required=True, nullable=False)
auth_parser.add_argument(name='role', type=str, location='json', required=False)

refresh_auth_parser: RequestParser = RequestParser()
refresh_auth_parser.add_argument(name="refresh_token", type=str, required=True, nullable=False)

tokens_parser: RequestParser = RequestParser()
tokens_parser.add_argument(name='access_token', type=str, required=False)
tokens_parser.add_argument(name='refresh_token', type=str, required=True)

change_password: RequestParser = RequestParser()
change_password.add_argument(name='old_password', type=str, required=True, nullable=False)
change_password.add_argument(name='new_password', type=str, required=True, nullable=False)

change_user_info_parser: RequestParser = RequestParser()
change_user_info_parser.add_argument(name='name', type=str, required=False)
change_user_info_parser.add_argument(name='surname', type=str, required=False)

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

movie_filter_and_page_parser: RequestParser = page_parser.copy()
movie_filter_and_page_parser.add_argument(name='director_id', type=int, location='args', required=False)
movie_filter_and_page_parser.add_argument(name='genre_id', type=int, location='args', required=False)
movie_filter_and_page_parser.add_argument(name='year', type=int, location='args', required=False)

movie_state_filter_and_page_parser: RequestParser = movie_filter_and_page_parser.copy()
movie_state_filter_and_page_parser.add_argument(
    name='status',
    choices=('new',),
    location='args',
    required=False,
    help='Only have to be "new"'
)
