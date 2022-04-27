import pathlib

from flask import Blueprint, Flask, jsonify, render_template, request, url_for
from nturl2path import url2pathname

from .models import CompressionService, db
from werkzeug.utils import secure_filename

compression_service_blueprint = Blueprint(
    "compression_service",
    __name__,
    template_folder="templates",
    static_folder="file_storage",
)


@compression_service_blueprint.route("/index")
def index():
    return "Hello, world!"


@compression_service_blueprint.route("/compress/<string:file_path>")
def compress(file_path):
    return "Compressing file: {}".format(file_path)


@compression_service_blueprint.route("/decompress/<string:file_path>")
def decompress(file_path):
    return "Decompressing file: {}".format(file_path)


# file upload endpoint
@compression_service_blueprint.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        # get the file from the request
        file = request.files["file"]
        print(file)
        # get the file name
        file_name = secure_filename(file.filename)
        print(file_name)
        # get pathlib to get the path to file_storage
        file_storage_path = str(pathlib.Path.cwd()) + str(pathlib.Path(r"\nuclei\compression_service\file_storage"))+str(rf"\{file_name}")
        print(file_storage_path)
        # save the file
        file.save(file_storage_path)
        # return the file path
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
