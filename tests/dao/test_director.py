import pytest
from werkzeug.exceptions import NotFound

from project.dao.main.director import DirectorDAO
from project.models import Director


class TestDirectorDAO:

    @pytest.fixture
    def director_dao(self, db):
        return DirectorDAO(db.session)

    @pytest.fixture
    def director_1(self, db):
        d = Director(name="Тейлор Шеридан")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def director_2(self, db):
        d = Director(name="Квентин Тарантино")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_director_by_id(self, director_1, director_dao):
        assert director_dao.get_by_id(director_1.id) == director_1

    def test_get_director_by_id_not_found(self, director_dao):
        with pytest.raises(NotFound):
            assert director_dao.get_by_id(3)

    def test_get_all_directors(self, director_dao, director_1, director_2):
        assert director_dao.get_all() == [director_1, director_2]

    def test_get_directors_by_page(self, app, director_dao, director_1, director_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert director_dao.get_all(1, app.config.get('ITEMS_PER_PAGE')) == [director_1]
        assert director_dao.get_all(2, app.config.get('ITEMS_PER_PAGE')) == [director_2]
        assert director_dao.get_all(3, app.config.get('ITEMS_PER_PAGE')) == []
