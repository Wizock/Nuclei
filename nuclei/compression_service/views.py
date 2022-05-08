import base64
import datetime
import hashlib
import os
import pathlib
import shutil
import sys

from flask import Blueprint, Flask, jsonify, redirect, render_template, request, url_for
from nturl2path import url2pathname
from PIL import Image
from sqlalchemy import false
from werkzeug.utils import secure_filename

compression_service_blueprint = Blueprint(
    "compression_service",
    __name__,
    template_folder="templates",
    url_prefix="/compression_service",
    static_folder="static/imgs",
)


from ..extension_globals.database import db
from .models import compression_index, media_index

@compression_service_blueprint.route("/display/compressed/<int:id>")
def display_compressed_id(id):
    # query all compression services
    compressed = compression_index.query.filter_by(id=id).first()
    if not compressed:
        return """<h1>No compressed images found</h1>  <a href='/compression_service/'>go to index</a>"""
    return render_template("individual_display.html", img=compressed, compressed=True)

@compression_service_blueprint.route("/display/uncompressed/<int:id>")
def display_uncompressed_id(id):
    # query all compression services
    uncompressed = compression_index.query.filter_by(id=id).first()
    if not uncompressed:
        return """<h1>No compressed images found</h1>  <a href='/compression_service/'>go to index</a>"""
    return render_template("individual_display.html", img=uncompressed, compressed=True)
























@compression_service_blueprint.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        file_name = secure_filename(file.filename)
        file_storage_path = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\static\imgs"))
            + str(rf"\{file_name}")
        )
        file.save(file_storage_path)
        # get file size
        file_size = os.path.getsize(file_storage_path)
        # get file hash
        file_hash_md5 = hashlib.md5(open(file_storage_path, "rb").read()).hexdigest()
        # get file base64
        file_base64 = base64.b64encode(open(file_storage_path, "rb").read()).decode(
            "utf-8"
        )
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
            file_size=file_size,
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
        return file_storage_path
    else:
        return """<!doctype html> <title>Upload new File</title> <h1>Upload new File</h1> <form method=post enctype=multipart/form-data> <input type=file name=file> <input type=submit value=Upload> </form>"""

@compression_service_blueprint.route("/index_design", methods=["POST", "GET"])
def index_design():
    # query media and compression models to get all media and compression objects
    media = media_index.query.all()
    compression = compression_index.query.all()
    # combine both lists
    combined = media + compression
    # sort combined list by date_created
    combined.sort(key=lambda x: x.date_created)
    # return index.html
    return render_template("dashboard.html", img=combined)

@compression_service_blueprint.route("/existing_compression/<file_name>")
def compress_uploaded(file_name):
    # check if file exists in database of either compressed or uncompressed files
    file_exists = media_index.query.filter_by(file_name=file_name).first()
    if file_exists:
        # check if file is already compressed
        check_compression = compression_index.query.filter_by(
            file_name=file_name
        ).first()
        if check_compression:
            # file is already compressed
            return redirect(url_for("compression_service.display_compressed"))
        else:
            file_path: str = (
                str(pathlib.Path.cwd())
                + str(pathlib.Path(r"\nuclei\compression_service\static\imgs"))
                + str(rf"\{file_name}")
            )
            file_path_compressed: str = (
                str(pathlib.Path.cwd())
                + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
                + str(rf"\{file_name}")
            )
            picture: Image = Image.open(file_path)
            picture.save(file_path_compressed, "JPEG", optimize=True, quality=85)
            file_size: int = os.path.getsize(file_path_compressed)
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
            compression_service: compression_index = compression_index(
                name=file_name,
                file_path=file_path,
                file_name=file_name,
                file_extension=file_extension,
                file_size=file_size,
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
            return file_path


@compression_service_blueprint.route("/compression_upload")
def compression_upload():
    if request.method == "POST":
        file = request.files["file"]
        file_name = secure_filename(file.filename)

        file_path_compressed: str = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
            + str(rf"\{file_name}")
        )
        picture: Image = Image.open(file_path)
        picture.save(file_path_compressed, "JPEG", optimize=True, quality=85)
        file_size: int = os.path.getsize(file_path_compressed)
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
        compression_service: compression_index = compression_index(
            name=file_name,
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            file_size=file_size,
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
        return file_path
    else:
        return """<!doctype html> <title>Compress a file</title> <h1>Compress a file</h1> <form method=post enctype=multipart/form-data> <input type=file name=file> <input type=submit value=Upload> </form>"""
