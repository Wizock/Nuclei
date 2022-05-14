import base64
import datetime
import hashlib
import os
import pathlib

from flask import Blueprint, Response, redirect, render_template, request, url_for
from .compression_preset import *
# import login required decorator
from flask_login import login_required
from PIL import Image
from werkzeug.utils import secure_filename

from ...extension_globals.database import db
from ..models import media_index
from ..views import compression_service_blueprint
def static_path_videos(file_name):
    file_path_static: str = (
        str(pathlib.Path.cwd())
        + str(pathlib.Path(r"\nuclei\compression_service\static\videos"))
        + str(rf"\{file_name}")
    )
    return file_path_static

def compressed_path(file_name):
    file_path_compressed: str = (
        str(pathlib.Path.cwd())
        + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
        + str(rf"\{file_name}")
    )
    return file_path_compressed

def commit_video(file):
    file_name = secure_filename(file.filename)
    file_storage_path = static_path_videos(file_name)
    file.save(file_storage_path)
    # get file size
    file_size = os.path.getsize(file_storage_path)
    # get file hash
    file_hash_md5 = hashlib.md5(open(file_storage_path, "rb").read()).hexdigest()
    # get file base64
    file_base64 = base64.b64encode(open(file_storage_path, "rb").read()).decode(
        "utf-8"
    )
    file_size_original = os.path.getsize(file_storage_path)
    # get file extension
    file_extension = os.path.splitext(file_storage_path)[1]
    # get file path
    file_path = os.path.dirname(file_storage_path)
    # create new CompressionService object
    compression_service = media_index(
        name=file_name,
        file_path=file_path,
        file_name=file_name,
        file_extension=file_extension,
        file_size_original=file_size_original,
        file_size_compressed=0,
        file_hash_md5=file_hash_md5,
        file_base64=file_base64,
        file_compressed=False,
        date_created=datetime.datetime.now(),
        date_updated=datetime.datetime.now(),
    )
    # add new CompressionService object to database
    db.session.add(compression_service)
    # commit changes to database
    db.session.commit()



def commit_video_compressed(file, preset=None):
    # secure the file size
    file_name = secure_filename(file.filename)
    # uncompressed file path
    file_path_static = static_path_videos(file_name)
    # compressed file path
    file_path_compressed = compressed_path(file_name)

    # compression algorithm
    try:
        file.save(file_path_static)
        # run the presetted video compression
        compression_main(file_path_compressed, file, preset=preset)
        # apply 
    except OSError as e:
        print(e)

    # committing code
    file_size_original = os.path.getsize(file_path_static)
    file_size_compressed: int = os.path.getsize(file_path_compressed)
    # get file hash
    file_hash_md5: str = hashlib.md5(
        open(file_path_compressed, "rb").read()
    ).hexdigest()
    # get file base64
    file_base64: str = base64.b64encode(
        open(file_path_compressed, "rb").read()
    ).decode("utf-8")
    # get file extension
    file_extension: str = os.path.splitext(file_path_compressed)[1]
    # get file path
    file_path: str = os.path.dirname(file_path_compressed)
    # create new CompressionService object
    compression_service: media_index = media_index(
        name=file_name,
        file_path=file_path,
        file_name=file_name,
        file_extension=file_extension,
        file_size_original=file_size_original,
        file_size_compressed=file_size_compressed,
        file_hash_md5=file_hash_md5,
        file_base64=file_base64,
        file_compressed=True,
        date_created=datetime.datetime.now(),
        date_updated=datetime.datetime.now(),
    )
    # add new CompressionService object to database
    db.session.add(compression_service)
    # commit changes to database
    db.session.commit()