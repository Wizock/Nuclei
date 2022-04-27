import os

from flask import Blueprint, Flask, jsonify, render_template, request, url_for

from .models import CompressionService, db

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
@compression_service_blueprint.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        # get the file from the request
        file = request.files["file"]
        # get the file name
        file_name = file.filename
        # get the file path
        file_path = os.path.join(url_for("compression_service.static"), file_name)
        # save the file
        file.save(file_path)
        # return the file path
        return file_path
    return render_template()
