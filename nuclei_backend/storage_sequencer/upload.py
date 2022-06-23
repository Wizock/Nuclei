from __future__ import annotations
import base64
import contextlib
import datetime
import hashlib
import logging
import os
import pathlib
import time
import celery
import typing
import requests
from flask import Response, request
from werkzeug.utils import secure_filename

from ..extension_globals.database import db
from .main import storage_sequencer_controller
from .model import FileTracker
from ..compression_service import media_index
from ..video_compression import video_media
import uuid

image_type = typing.Union[str, bytes]
video_type = typing.Union[str, bytes]


def allowed_file(filename: str) -> bool:
    if "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "png",
        "jpg",
        "jpeg",
    ]:
        # check if the file exists in the media_index table
        if media_index.query.filter_by(file_name=filename).first():
            # return the file with the image type
            return filename:= image_type
    if "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "mp4",
        "mov",
        "avi",
    ]:
        # check if the file exists in the media_index table
        if video_media.query.filter_by(file_name=filename).first():
            return filename:= video_type
    return False


def return_file_path(filename: typing.Callable) -> str:
    if filename == image_type:
        # check if the file exists in the media_index table
        if media_index.query.filter_by(file_name=filename).first():
            return media_index.query.filter_by(file_name=filename).first().file_path
        # check if the file exists in the media_index table
    if filename == video_type: 
        video_media.query.filter_by(file_name=filename).first().file_path
        return video_media.query.filter_by(file_name=filename).first().file_path

@celery.task
def produce_cid(file: str):
    """
    Produce a CID for a file.
    """
    unique_id = str(uuid.uuid4())
    file_type = file.split(".")[-1]
    try:
        # check if the file exists in the media_index model
        file_tracker = FileTracker.query.filter_by(file_name=file).first()
        if file_tracker:
            # if the file exists, return the CID
            return file_tracker.cid

        if os.path.isfile(file):
            for _ in range(0, 3):
                if _ == 2:
                    return "Error: IPFS hash not found."
                if os.path.isfile(f"temp{unique_id}.txt"):
                    os.system(
                        "ipfs add --quiet --pin {file}.{file_type} > temp{unique_id}.txt"
                    )
                    with open("temp.txt", "r+") as f:
                        ipfs_hash = f.read()
                    break
                else:
                    open(f"temp{unique_id}.txt", "w+")
                    continue
        else:
            raise Exception("File does not exist.")
    except Exception as e:
        logging.error(e)
    os.remove("temp.txt")
    return ipfs_hash


@storage_sequencer_controller.route("/upload/<string:file>", methods=["GET", "POST"])
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

        file_record = FileTracker(
            file_name=filename,
            file_path=file.filename,
            file_hash=ipfs_hash,
            file_size=file.content_length,
            file_type=file.content_type,
            file_date=datetime.datetime.now(),
        )
        db.session.add(file_record)
        db.session.commit()
    else:
        return Response(
            "File type not allowed.",
            status=400,
            mimetype="text/plain",
        )
