from .genres import genres_ns
from .movies import movies_ns
from .directors import directors_ns
from .user import api as user_ns

__all__ = [
    'genres_ns',
    'movies_ns',
    'directors_ns',
    'user_ns'
]
