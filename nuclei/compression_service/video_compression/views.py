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
from .commit_shorthands import *
from .compression_preset import compression_main

# upload a video route
@compression_service_blueprint.route("/upload/video", methods=["POST", "GET"])
def upload_video():
    if request.method == "POST":
        commit_video(request.files["file"])
        return redirect(url_for("compression_service.index_design"))
    else:
        return render_template("upload_template.html")

@compression_service_blueprint.route("/compress/video", methods=["POST", "GET"])
def compress_video():
    if request.method == "POST":
        # get file name
        file_name = request.form["file_name"]
        try:
            commit_video_compressed(file_name, compression_main(file_name))
        except Exception as e:
            return e
        finally:
            return redirect(url_for("compression_service.index_design"))
    else:
        return render_template("video_compression_upload.html")





@compression_service_blueprint.route(
    "/compress/video/<video_name>/<video_id>/<preset>", methods=["POST", "GET"]
)
def compress_video_presetted(video_name: str, video_id: int, preset: str):
    return "compress_video"

# get the status of a video
@compression_service_blueprint.route("/status/video", methods=["POST", "GET"])
def status_video():
    return "status_video"


# compress already uploaded video
@compression_service_blueprint.route("/compressed/video", methods=["POST", "GET"])
def compressed_video(name):
        # check if file exists in database of either compressed or uncompressed files
    file_is_compressed = media_index.query.filter_by(
        id=id, file_name=name, file_compressed=True
    ).first()
    if file_is_compressed:
        return redirect(f"/compression_service/display/compressed/{id}/{name}")
    else:
        file_path: str = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\static\imgs"))
            + str(rf"\{name}")
        )
        file_path_compressed: str = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
            + str(rf"\{name}")
        )
        try:
            picture: Image = Image.open(file_path)
            picture.save(file_path_compressed, "JPEG", optimize=True, quality=85)
        except OSError as e:
            print(e)
        finally:
            picture: Image = Image.open(file_path)
            rgb_im = picture.convert("RGB")
            rgb_im.save(file_path_compressed, "JPEG", optimize=True, quality=85)
        file_size_orignal = os.path.getsize(file_path)
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
        try:
            compression_service: media_index = media_index.query.get(id)
            compression_service.file_path = file_path
            compression_service.file_name = name
            compression_service.file_extension = file_extension
            compression_service.file_size_orignal = file_size_orignal
            compression_service.file_size_compressed = file_size_compressed
            compression_service.file_hash_md5 = file_hash_md5
            compression_service.file_base64 = file_base64
            compression_service.file_compressed = True
            compression_service.date_updated = datetime.datetime.now()
            db.session.commit()
        except Exception as e:
            print(e)
        return redirect(f"/compression_service/display/compressed/{id}/{name}")
