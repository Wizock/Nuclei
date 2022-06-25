from __future__ import annotations

import contextlib
import datetime
import logging
import os
import pathlib
import typing
import uuid
import subprocess

import gevent
from flask import Response, request
from werkzeug.utils import secure_filename

from ..compression_service.models import media_index
from ..extension_globals.celery import celery
from ..extension_globals.database import db
from .file_info_utils import allowed_file, return_file_path
from ..video_compression.models import video_media
from .main import storage_sequencer_controller
from .model import FileTracker


def check_if_temp_exist(file_name: str) -> bool:
    """
    Checks if the file is in the temp folder
    :param file_name: The file name
    :return: True if the file is in the temp folder, False otherwise
    """
    temp_folder = storage_sequencer_controller.config.TEMP_FOLDER
    if os.path.isfile(os.path.join(temp_folder, file_name)):
        return True
    return False


@celery.task
def produce_cid(file: str):
    """
    Produce a CID for a file. using celery and gevent to handle traffic
    Args:
        file: The file to produce a CID for.
    """

    unique_id = str(uuid.uuid4())
    file_type = str(file).split(".")[-1]
    file_name = str(file).split("/")[-1]
    logging.info(f"Producing CID for {file_name}")
    path = storage_sequencer_controller.config.TEMP_FOLDER
    logging.info(path)

    with open(
        os.path.join(path, "upload.bat"),
        "w",
    ) as f:
        f.write(
            f"ipfs add --quiet --pin {file_name}.{file_type} > {path}/temp{unique_id}.txt"
        )
    subprocess.call(
        os.path.join(storage_sequencer_controller.config.TEMP_FOLDER, "upload.bat")
    )

    with open(
        os.path.join(
            storage_sequencer_controller.config.TEMP_FOLDER, f"temp{unique_id}.txt"
        ),
        "r",
    ) as f:
        cid = f.read().strip()

    os.remove(
        os.path.join(
            storage_sequencer_controller.config.TEMP_FOLDER, f"temp{unique_id}.txt"
        )
    )
    # os.remove(
    #     os.path.join(
    #         storage_sequencer_controller.config.TEMP_FOLDER, f"{file}.{file_type}"
    #     )
    # )

    return cid


@storage_sequencer_controller.route("/upload", methods=["POST", "PUT"])
@celery.task
def ipfs_upload():
    """
    Upload a file to IPFS.

    Args:
        file: The file to upload.
    """
    file = request.files["files"]
    logging.info(f"Uploading {file} to IPFS")
    # using celery and gevent to handle traffic
    # check if there are multiple requests of this route using gevent
    if file in request.files:
        # if there are multiple requests for this file, spawn a new greenlet task to handle the request
        return "Error: Multiple requests for this file."
    if file.filename == "":
        return "Error: No file selected."
    # check if the file is one of the allowed types/extensions
    # if file and allowed_file(file.filename):
    # file is allowed, move it to the upload folder
    filename = secure_filename(file.filename)
    ipfs_hash = produce_cid(file)
    logging.info(f"IPFS hash: {ipfs_hash}")
    # ipfs_hash = ipfs_hashS
    if ipfs_hash == "Error: IPFS hash not found.":
        return ipfs_hash

    file_record = FileTracker(
        file_name=str(filename),
        file_path=str(file.filename),
        file_hash=str(ipfs_hash),
        file_size=int(file.content_length),
        file_type=str(file.content_type),
        file_date=datetime.datetime.now(),
    )

    # db.session.add(file_record)
    # db.session.commit()
    return Response(ipfs_hash, status=200, mimetype="text/plain")
    # return Response("Error: File type not allowed.", status=400, mimetype="text/plain")
