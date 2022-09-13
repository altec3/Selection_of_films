import pytest
from werkzeug.exceptions import NotFound

from project.dao.main.genre import GenreDAO
from project.models import Genre


class TestGenresDAO:

    @pytest.fixture
    def genres_dao(self, db):
        return GenreDAO(db.session)

    @pytest.fixture
    def genre_1(self, db):
        g = Genre(name="Боевик")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def genre_2(self, db):
        g = Genre(name="Комедия")
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_genre_by_id(self, genre_1, genres_dao):
        assert genres_dao.get_by_id(genre_1.id) == genre_1

    def test_get_genre_by_id_not_found(self, genres_dao):
        with pytest.raises(NotFound):
            assert genres_dao.get_by_id(3)

    def test_get_all_genres(self, genres_dao, genre_1, genre_2):
        assert genres_dao.get_all() == [genre_1, genre_2]

    def test_get_genres_by_page(self, app, genres_dao, genre_1, genre_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert genres_dao.get_all(1, app.config.get('ITEMS_PER_PAGE')) == [genre_1]
        assert genres_dao.get_all(2, app.config.get('ITEMS_PER_PAGE')) == [genre_2]
        assert genres_dao.get_all(3, app.config.get('ITEMS_PER_PAGE')) == []
