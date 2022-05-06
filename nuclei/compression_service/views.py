import base64
import hashlib
import os
import pathlib
import shutil
from pyguetzli import GueltZip

from flask import Blueprint, Flask, jsonify, render_template, request, url_for
from nturl2path import url2pathname
from werkzeug.utils import secure_filename

compression_service_blueprint = Blueprint(
    "compression_service",
    __name__,
    template_folder="templates",
    static_folder="/file_storage/",
)

from ..extension_globals.database import db
from .models import CompressionService


@compression_service_blueprint.route("/")
def index():
    # query all compression services
    compression_services = CompressionService.query.all()
    return render_template("indexer.html", compression_services=compression_services)


# file upload endpoint
@compression_service_blueprint.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        file = request.files["file"]

        file_name = secure_filename(file.filename)
        file_storage_path = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\file_storage"))
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
        compression_service = CompressionService(
            name=file_name,
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            file_size=file_size,
            file_hash_md5=file_hash_md5,
            file_base64=file_base64,
        )
        # add new CompressionService object to database
        db.session.add(compression_service)
        # commit changes to database
        db.session.commit()

        return file_storage_path
    else:
        return """
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
        """
