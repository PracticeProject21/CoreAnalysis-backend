import pytest

from backend import create_app
from backend.database import db


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def client2():
    app = create_app(**{'TESTING': True, 'DATABASE': "sqlite:///"})

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client
