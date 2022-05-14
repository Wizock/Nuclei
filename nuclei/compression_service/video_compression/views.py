import base64
import datetime
import hashlib
import os
import pathlib

from flask import Blueprint, Response, redirect, render_template, request, url_for

# import login required decorator
from flask_login import login_required
from PIL import Image
from werkzeug.utils import secure_filename

from ...extension_globals.database import db
from ..models import media_index
from ..views import compression_service_blueprint
from .compression_preset import compression_main


@compression_service_blueprint.route("/upload/video", methods=["GET", "POST"])
def upload_video():
    if request.method == "POST":
        if request.files:
            video_file = request.files["file"]
            video_name = video_file.filename
            file_path: str = (
                str(pathlib.Path.cwd())
                + str(pathlib.Path(r"\nuclei\compression_service\static\videos"))
                + str(rf"\{video_name}")
            )

            video_file.save(file_path)
            file_size_original = os.path.getsize(file_path)
            file_size_compressed: int = 0
            # get file hash
            file_hash_md5: str = hashlib.md5(open(file_path, "rb").read()).hexdigest()
            # get file base64
            file_base64: str = base64.b64encode(open(file_path, "rb").read()).decode(
                "utf-8"
            )
            # get file extension
            file_extension: str = os.path.splitext(file_path)[1]
            # get file path
            file_path: str = os.path.dirname(file_path)
            # create new CompressionService object
            compression_service: media_index = media_index(
                name=video_name,
                file_path=file_path,
                file_name=video_name,
                file_extension=file_extension,
                file_size_original=file_size_original,
                file_size_compressed=file_size_compressed,
                file_hash_md5=file_hash_md5,
                file_base64=file_base64,
                file_compressed=True,
                date_created=datetime.datetime.now(),
                date_updated=datetime.datetime.now(),
            )
            db.session.add(compression_service)
            db.session.commit()

    return render_template("upload_template.html")


@compression_service_blueprint.route("/compress/video", methods=["GET"])
def compress_video():
    if request.method == "POST":
        if request.files:
            video_file = request.files["file"]
            video_name = video_file.filename
            file_path: str = (
                str(pathlib.Path.cwd())
                + str(pathlib.Path(r"\nuclei\compression_service\static\videos"))
                + str(rf"\{video_name}")
            )
            file_path_compressed: str = (
                str(pathlib.Path.cwd())
                + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
                + str(rf"\{video_name}")
            )

            video_file.save(file_path)

            compression_main(file_path, file_path_compressed, preset="perfect")

            file_size_original = os.path.getsize(file_path)
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
                name=video_name,
                file_path=file_path,
                file_name=video_name,
                file_extension=file_extension,
                file_size_original=file_size_original,
                file_size_compressed=file_size_compressed,
                file_hash_md5=file_hash_md5,
                file_base64=file_base64,
                file_compressed=True,
                date_created=datetime.datetime.now(),
                date_updated=datetime.datetime.now(),
            )
            db.session.add(compression_service)
            db.session.commit()

    return render_template("upload_template.html")


@compression_service_blueprint.route("/compressed/video", methods=["GET"])
def compressed_video():
    return render_template("compression_service/compressed_video.html")
