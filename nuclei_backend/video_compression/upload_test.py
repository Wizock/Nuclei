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
    files={"files": open(pathlib.Path(__file__).parent.absolute() / "test.mp4", "rb")},
)
# file_non_compression = open(
#     pathlib.Path(__file__).parent.absolute() / "file_non_compression.txt", "w"
# )
# file_non_compression.write(
#     f"The upload response status code is {req_norm.status_code} and the body is {req_norm.text}"
# )

file_compression = open(
    pathlib.Path(__file__).parent.absolute() / "file_compression.txt", "w"
)
file_compression.write(
    f"The upload response status code is {req_comp.status_code} and the body is {req_comp.text}"
)
