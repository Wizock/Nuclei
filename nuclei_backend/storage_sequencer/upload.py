import contextlib
import logging
import os

import requests
from flask import Response, request
from werkzeug.utils import secure_filename

from .main import storage_sequencer_controller
from .model import file_tracker


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "png",
        "jpg",
        "jpeg",
    ]


@contextlib.contextmanager
def produce_cid(file: str):
    """
    Produce a CID for a file.
    """
    try:
        if os.path.isfile(file):
            for _ in range(0, 3):
                if _ == 2:
                    return "Error: IPFS hash not found."
                if os.path.isfile("temp.txt"):
                    os.system("ipfs add --quiet --pin upload.txt > temp.txt")
                    with open("temp.txt", "r+") as f:
                        ipfs_hash = f.read()
                    break
                else:
                    open("temp.txt", "w+")
                    continue
        else:
            raise Exception("File does not exist.")
    except Exception as e:
        logging.error(e)
    os.system("rm temp.txt")
    return ipfs_hash


@storage_sequencer_controller.route("/upload/<file:file>", methods=["POST"])
@contextlib.contextmanager
def ipfs_upload(file):
    """
    Upload a file to IPFS.
    """
    file = request.files["file"]
    # check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # file is allowed, move it to the upload folder
        filename = secure_filename(file.filename)
        ipfs_hash = produce_cid(file)

        file_record = file_tracker(
            file_name=filename,
            file_type=filename.rsplit(".", 1)[1].lower(),
            file_hash=ipfs_hash,
            file_size=file.content_length,
            file_status="uploaded",
        )
    else:
        return Response(
            "File type not allowed.",
            status=400,
            mimetype="text/plain",
        )
