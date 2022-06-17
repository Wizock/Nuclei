from ..authentication.models import User
from .authentication_test import *
from .main_tests import *


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login(client):
    # test a post request for login, should redirect to index else return a 300
    assert client.get("/login").status_code == 200
    assert (
        client.post("/login", data={"email": "test", "password": "test"}).status_code
        == 200
    )


def test_incorrect_login(client):
    assert (
        client.post("/login", data={"email": "test", "password": "test1"}).status_code
        == 302
    )


def test_register(client):
    # if user exists return a 302

    assert client.get("/register").status_code == 200
    assert (
        client.post(
            "/register", data=dict(username="test", password="test", email="test")
        ).status_code
        == 302
    )


def test_register_redirect(client, app):
    assert client.get("/register").status_code == 200
    assert (
        client.post(
            "/register", data=dict(username="test", password="test", email="test")
        ).status_code
        == 302
    )

    with app.app_context():
        assert User.query.filter_by(username="test").first() is not None
