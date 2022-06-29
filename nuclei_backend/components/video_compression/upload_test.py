import pathlib

import requests

multiple_files = [
    (
        "files",
        (
            "second.mkv",
            open(pathlib.Path(__file__).parent.absolute() / "second.mkv", "rb"),
            "video/mp4",
        ),
    ),
    (
        "files",
        (
            "test.mp4",
            open(pathlib.Path(__file__).parent.absolute() / "test.mp4", "rb"),
            "video/mp4",
        ),
    ),
]


requests.post(
    url="http://localhost:5000/storage/upload",
    files=multiple_files,
)
