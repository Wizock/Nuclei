from __future__ import annotations

import contextlib
import datetime
import logging
import os
import typing
import uuid
import gevent
from flask import Response, request
from werkzeug.utils import secure_filename

from ..compression_service.models import media_index
from ..extension_globals.database import db
from ..video_compression.models import video_media
from .main import storage_sequencer_controller
from .model import FileTracker
from ..extension_globals.celery import celery


image_type = typing.Union[str, bytes]
video_type = typing.Union[str, bytes]


def allowed_file(filename: typing.AnyStr) -> bool:
    if "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "png",
        "jpg",
        "jpeg",
    ]:
        # check if the file exists in the media_index table
        if media_index.query.filter_by(file_name=filename).first():
            # return the file with the image type
            filename = image_type
            return filename
    if "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "mp4",
        "mov",
        "avi",
    ]:
        # check if the file exists in the media_index table
        if video_media.query.filter_by(file_name=filename).first():
            filename = video_type
            return filename
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
@contextlib.contextmanager
def produce_cid(file: str):
    """
    Produce a CID for a file. using celery and gevent to handle traffic
    Args:
        file: The file to produce a CID for.
    """
    # using celery and gevent to handle traffic
    with contextlib.closing(gevent.spawn(produce_cid, file)) as task:
        unique_id = str(uuid.uuid4())
        file_type = file.split(".")[-1]
        try:
            # check if the file exists in the media_index model
            file_tracker = FileTracker.query.filter_by(file_name=file).first()
            if file_tracker:
                # if the file exists, return the CID
                return file_tracker.cid

            if return_file_path(allowed_file(file.filename)):
                for _ in range(0, 3):
                    if _ == 2:
                        return "Error: IPFS hash not found."
                    if os.path.isfile(f"temp{unique_id}.txt"):
                        os.system(
                            f"ipfs add --quiet --pin {file}.{file_type} > temp{unique_id}.txt"
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
        yield ipfs_hash


@storage_sequencer_controller.route("/upload/<string:file>", methods=["POST"])
@celery.task
async def ipfs_upload(file):
    """
    Upload a file to IPFS.

    Args:

        file: The file to upload.

    """

    # using celery and gevent to handle traffic
    with contextlib.closing(gevent.spawn(ipfs_upload, file)) as task:
        # check if there are multiple requests of this route using gevent
        if file in request.files:
            # if there are multiple requests for this file, spawn a new greenlet task to handle the request
            return "Error: Multiple requests for this file."
        file = request.files["file"]
        if file.filename == "":
            return "Error: No file selected."
        # check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # file is allowed, move it to the upload folder
            filename = secure_filename(file.filename)
            ipfs_hash = gevent.spawn(produce_cid(file), file)
            ipfs_hash = ipfs_hash.get()
            if ipfs_hash == "Error: IPFS hash not found.":
                return ipfs_hash

            file_record = FileTracker(
                file_name=filename,
                file_path=file.filename,
                file_hash=ipfs_hash,
                file_size=file.content_length,
                file_type=file.content_type,
                file_date=datetime.datetime.now(),
            )

            db.session.add(file_record)
            await db.session.commit()
            return Response(
                "File uploaded successfully.", status=200, mimetype="text/plain"
            )
