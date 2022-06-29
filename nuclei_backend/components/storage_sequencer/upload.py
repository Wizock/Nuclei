from __future__ import annotations

import contextlib
import datetime
import hashlib
import logging
import os
import pathlib
from subprocess import PIPE, Popen, call
from typing import *
from uuid import UUID, uuid4

import gevent
from flask import Response, request
from typing_extensions import LiteralString
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ...extension_globals.celery import celery
from ...extension_globals.database import db
from ..compression_service.models import media_index
from .file_info_utils import allowed_file, return_file_path
from .main import storage_sequencer_controller
from .model import FileTracker


def check_if_temp_exist(file_name: str) -> bool:
    """
    _summary_: Check if the temp file exists
    _parameters_:
        file_name: str
    _return_: bool
    """
    temp_folder = storage_sequencer_controller.config.TEMP_FOLDER
    if os.path.isfile(os.path.join(temp_folder, file_name)):
        return True
    return False


def cleanup(unique_id: UUID, path: pathlib.Path, file_name: str):
    """
    Cleanup the file from the temp folder.
    Args:
        unique_id (UUID): the unique identifier for file
        path (pathlib.Path): the path of the file to be cleaned up
        file_name (str): the name of the file to be cleaned up
    """


def generate_hash(cid: LiteralString) -> LiteralString:

    """
    Generate a hash for the file.
    Args:
        cid: The cid of the file.
    Usage:
    >>> hash = generate_hash(cid)
    """
    path = str(storage_sequencer_controller.config.TEMP_FOLDER)
    unique_id = str(uuid4())

    with open(
        os.path.join(path, f"hash{unique_id}.bat"),
        "w",
    ) as f:
        f.write(rf"cd {path}")
        f.write("\n")
        f.write(rf"ipfs ls -v {cid} > hash{unique_id}.txt")
    call(
        os.path.join(
            storage_sequencer_controller.config.TEMP_FOLDER, f"hash{unique_id}.bat"
        )
    )

    with open(
        os.path.join(
            storage_sequencer_controller.config.TEMP_FOLDER, f"hash{unique_id}.txt"
        ),
        "r",
    ) as f:
        hash = f.read().strip()

    os.remove(
        os.path.join(
            storage_sequencer_controller.config.TEMP_FOLDER, f"hash{unique_id}.bat"
        )
    )
    os.remove(
        os.path.join(
            storage_sequencer_controller.config.TEMP_FOLDER, f"hash{unique_id}.txt"
        )
    )

    return hash


@celery.task
def produce_cid(file: FileStorage) -> LiteralString:
    """
    Produce a CID for a file. using celery and gevent to handle traffic
    Args:
        file: The file to produce a CID for.
    Returns:
        A CID for the file.
        >>> produce_cid(file)
        >>> QmegzqBL9FpNCHjgNwY3aEKq1ADp7JUonDb5K23QLmbh43y
    """

    unique_id = str(uuid4())
    file_name = secure_filename(file.filename)
    file_extension = file_name.split(".")[-1]
    path = str(storage_sequencer_controller.config.TEMP_FOLDER)
    with open(
        os.path.join(path, f"upload{unique_id}.bat"),
        "w",
    ) as f:
        f.write(rf"cd {path}")
        f.write("\n")
        f.write(rf"ipfs add --quiet --pin {file_name} > {path}\temp{unique_id}.txt")
    call(
        os.path.join(
            storage_sequencer_controller.config.TEMP_FOLDER, f"upload{unique_id}.bat"
        )
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
    os.remove(os.path.join(storage_sequencer_controller.config.TEMP_FOLDER, file_name))
    os.remove(
        os.path.join(
            storage_sequencer_controller.config.TEMP_FOLDER, f"upload{unique_id}.bat"
        )
    )

    return cid


def assemble_record(file: FileStorage, cid: LiteralString) -> FileTracker:
    """
    Assembles a record for the file tracker
    Args:
        file: The file to assemble a record for
        cid: The cid of the file
    Returns:
        A record for the file tracker
        >>> assemble_record(file, cid)
        >>> FileTracker( file_name='test.mp4',
        >>>             file_type='video',
        >>>             file_size=12345,
        >>>             file_hash='QmegzqBL9FpNCHjgNwY3aEKq1ADp7JUonDb5K23QLmbh43y',
        >>>             file_cid='QmegzqBL9FpNCHjgNwY3aEKq1ADp7JUonDb5K23QLmbh43y',
        >>>             file_upload_date=datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc),
    """
    file_name = secure_filename(file.filename)
    file_cid = cid
    file_hash = generate_hash(cid)
    file_size = os.path.getsize(file.stream.fileno())
    file_type = understand_filetype(file)
    file_date = datetime.datetime.now()
    file_index = FileTracker(
        file_name=file_name,
        file_cid=file_cid,
        file_hash=file_hash,
        file_size=file_size,
        file_type=file_type,
        file_date=file_date,
    )

    return file_index


def understand_filetype(file: FileStorage) -> Literal["video", "image", "audio"]:
    """
    Determine the file type of a file.
    Args:
        file: The file to determine the file type of.
    Usage:
    >>> file_type = understand_filetype(file)
    >>> "Video"
    """
    try:
        if allowed_file(file.filename):
            if file.content_type == "video/mp4":
                return "video"
            elif file.content_type == "image/jpeg":
                return "image"
            else:
                return "file"
        else:
            return "invalid"
    except Exception as e:
        return "invalid"


@storage_sequencer_controller.route("/upload", methods=["POST", "PUT"])
@celery.task
def ipfs_upload() -> Response:
    """
    Upload a file to IPFS.
    Returns:
        A response with the CID of the file.
    """
    if request.method == "POST":
        file = request.files["files"]
        file.save(
            os.path.join(storage_sequencer_controller.config.TEMP_FOLDER, file.filename)
        )
        file_type = understand_filetype(file)

        cid = produce_cid(file)

        record = assemble_record(file, cid)

        db.session.add(record)

        db.session.commit()

        return Response(cid, mimetype="text/plain", status=200)
