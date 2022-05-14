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

@compression_service_blueprint.route("/upload/video", methods=["GET","POST"])
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
            file_path_compressed: str = (
                str(pathlib.Path.cwd())
                + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
                + str(rf"\{video_name}")
            )
            video_file.save(file_path)

            compression_main(file_path, file_path_compressed)

            return redirect(url_for("compression_service.compressed_video"))
    return render_template("upload_template.html")

@compression_service_blueprint.route("/compress/video", methods=["GET"])
def compress_video():
    return render_template("compression_service/compress_video.html")

@compression_service_blueprint.route("/compressed/video", methods=["GET"])
def compressed_video():
    return render_template("compression_service/compressed_video.html")

