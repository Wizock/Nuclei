import pathlib

import requests

# make a post request to the /video_compression/upload/video endpoint
# with the video file as the payload
# the response should be a redirect to the /video_compression/upload/video endpoint

# req_norm = requests.post(
#     "http://10.1.1.41:5000/video_compression/upload/video",
#     files={"file": open(pathlib.Path(__file__).parent.absolute() / "test.mp4", "rb")},
# )
req_comp = requests.post(
    "http://10.1.1.41:5000/storage/upload",
    files={"files": open(pathlib.Path(__file__).parent.absolute() / "data.pdf", "rb")},
)
