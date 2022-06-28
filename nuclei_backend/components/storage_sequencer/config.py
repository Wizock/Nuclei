import pathlib
from importlib.resources import path

from git import Object


class storage_sequence_config(Object):

    IPFS_CONNECT_URL = "/ip4/127.0.0.1/tcp/5001/http"
    IPFS_FILE_URL = "http://127.0.0.1:8080/ipfs/"
    DOMAIN = "http://localhost:5000"
    # get the full path to the temp folder
    TEMP_FOLDER = pathlib.Path(__file__).parent.joinpath("temp_")
