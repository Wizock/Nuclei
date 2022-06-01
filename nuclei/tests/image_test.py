from pathlib import Path

from .authentication_test import *
from .main_tests import *

resources = Path(__file__).parent / "resources"


def test_image_index(client):
    response = client.post("/login", data={"email": "test", "password": "test"})
    response = client.get("compression_service/compression_upload")

    assert response.status_code == 200


def injection_compression_test(client):
    response = client.post("/login", data={"email": "test", "password": "test"})
    response = client.post(
        "compression_service/compression_upload",
        data={"file": (resources / "input.jpeg").open("rb")},
    )

    assert response.status_code == 200


def test_compression_upload(client):
    response = client.post("/login", data={"email": "test", "password": "test"})
    response = client.post(
        "compression_service/compression_upload",
        data={"file": (resources / "input.jpeg").open("rb")},
    )

    assert response.status_code == 400


def test_compression_upload_invalid_file(client):
    response = client.post("/login", data={"email": "test", "password": "test"})

    response = client.post(
        "compression_service/compression_upload",
        data={"file": (resources / "input.txt").open("rb")},
    )

    assert response.status_code == 400


def test_compression_upload_no_file(client):
    response = client.post("/login", data={"email": "test", "password": "test"})

    response = client.post(
        "compression_service/compression_upload",
        data={"file": ""},
    )

    assert response.status_code == 302
