from pathlib import Path

from .authentication_test import *
from .main_tests import *

resources = Path(__file__).parent / "resources"


def test_video_index(client):
    response = client.post("/login", data={"email": "test", "password": "test"})
    response = client.get("/video_compression/upload/video")
    assert response.status_code == 200


def test_video_upload_invalid_file(client):
    response = client.post("/login", data={"email": "test", "password": "test"})

    response = client.post(
        "/video_compression/upload/video",
        data={"file": (resources / "input.txt").open("rb")},
    )

    assert response.status_code == 302


def test_video_upload_no_file(client):
    response = client.post("/login", data={"email": "test", "password": "test"})

    response = client.post(
        "/video_compression/upload/video",
        data={"file": ""},
    )

    assert response.status_code == 302


def test_video_upload_invalid_file_type(client):
    response = client.post("/login", data={"email": "test", "password": "test"})

    response = client.post(
        "/video_compression/upload/video",
        data={"file": (resources / "input.mp4")},
    )

    assert response.status_code == 200
