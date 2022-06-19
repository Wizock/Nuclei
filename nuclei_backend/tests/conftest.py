from .main_tests import *


class TestAuthentication:
    def __init__(self, client):
        self._client = client

    def test_login_view(self, username="test", password="test"):
        return self._client.post(
            "/login", data={"email": username, "password": password}
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return TestAuthentication(client)
