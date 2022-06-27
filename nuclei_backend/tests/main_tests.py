import pytest

import nuclei_backend


@pytest.fixture
def app():
    app = nuclei_backend.app
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
