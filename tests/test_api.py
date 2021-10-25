from flask.testing import FlaskClient

from fixtures import *


def test_CORS(client: FlaskClient):
    assert client.get('/').headers['Access-Control-Allow-Origin'] == '*'
