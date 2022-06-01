from pathlib import Path

from .authentication_test import *
from .main_tests import *

resources = Path(__file__).parent / "resources"


def test_video_index(client):
    response = client.post("/login", data={"email": "test", "password": "test"})
    response = client.get("video_service/video_upload")

    assert response.status_code == 200


def injection_video_test(client):
    response = client.post("/login", data={"email": "test", "password": "test"})
    response = client.post(
        "video_service/video_upload",
        data={"file": (resources / "input.jpeg").open("rb")},
    )

    assert response.status_code == 200


def test_video_upload(client):
    response = client.post("/login", data={"email": "test", "password": "test"})
    response = client.post(
        "video_service/video_upload",
        data={"file": (resources / "input.jpeg").open("rb")},
    )

    assert response.status_code == 400


def test_video_upload_invalid_file(client):
    response = client.post("/login", data={"email": "test", "password": "test"})

    response = client.post(
        "video_service/video_upload",
        data={"file": (resources / "input.txt").open("rb")},
    )

    assert response.status_code == 400


def test_video_upload_no_file(client):
    response = client.post("/login", data={"email": "test", "password": "test"})

    response = client.post(
        "video_service/video_upload",
        data={"file": ""},
    )

    assert response.status_code == 302


def test_video_upload_invalid_file_type(client):
    response = client.post("/login", data={"email": "test", "password": "test"})

    response = client.post(
        "video_service/video_upload",
        data={"file": (resources / "input.mp4").open("rb")},
    )

    assert response.status_code == 400
