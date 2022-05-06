from flask import Blueprint, Flask, jsonify, render_template, request, url_for
import base64, hashlib, os, shutil, pathlib, sys
from werkzeug.utils import secure_filename
from nturl2path import url2pathname
from PIL import Image


compression_service_blueprint = Blueprint(
    "compression_service",
    __name__,
    template_folder="templates",
    url_prefix="/compression_service",
    static_folder="static/imgs",
)


from ..extension_globals.database import db
from .models import media_index, compression_index


@compression_service_blueprint.route("/disp")
def display():
    # query all compression services
    compression_services = media_index.query.all()

    return render_template("index.html", img=compression_services)

# file upload endpoint
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
        file_base64 = base64.b64encode(open(file_storage_path, "rb").read()).decode("utf-8")
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
        )
        # add new CompressionService object to database
        db.session.add(compression_service)
        # commit changes to database
        db.session.commit()
        return file_storage_path
    else:
        return """<!doctype html> <title>Upload new File</title> <h1>Upload new File</h1> <form method=post enctype=multipart/form-data> <input type=file name=file> <input type=submit value=Upload> </form>"""

@compression_service_blueprint.route("/compress/<file_name>")
def compression(file_name):
    # get file path
    file_path = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\static\imgs"))
            + str(rf"\{file_name}")
        )
    file_path_compressed = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
            + str(rf"\{file_name}")
        )
    
    picture = Image.open(file_path)
    picture.save(file_path_compressed, "JPEG", optimize=True, quality=50)
    file_size = os.path.getsize(file_path_compressed)
        # get file hash
    file_hash_md5 = hashlib.md5(open(file_path_compressed, "rb").read()).hexdigest()
    # get file base64
    file_base64 = base64.b64encode(open(file_path_compressed, "rb").read()).decode("utf-8")
    # get file extension
    file_extension = os.path.splitext(file_path_compressed)[1]
    # get file path
    file_path = os.path.dirname(file_path_compressed)
    # create new CompressionService object
    compression_service = compression_index(
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
    
    return file_path