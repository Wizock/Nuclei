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

compression_service_blueprint = Blueprint(
    "compression_service",
    __name__,
    template_folder="templates",
    url_prefix="/compression_service",
    static_folder="static/imgs",
)

from ..extension_globals.celery import celery
from ..extension_globals.database import db
from .models import media_index


@compression_service_blueprint.route("/")
@compression_service_blueprint.route("/index_design", methods=["POST", "GET"])
@login_required
@celery.task
def index_design():
    # query media models to get all media objects
    media = media_index.query.all()
    media.sort(key=lambda x: x.date_created)
    return render_template("dashboard.html", img=media)


@compression_service_blueprint.route("/display/compressed/<int:id>/<string:name>")
@login_required
@celery.task
def display_compressed_id(id: int, name: str):
    # query all compression services
    compressed = media_index.query.filter_by(
        id=id, file_name=name, file_compressed=True
    ).first()
    if not compressed:
        return """<h1>No compressed images found</h1>  <a href='/compression_service/'>go to index</a>"""
    return render_template("individual_display.html", img=compressed, compressed=True)


@compression_service_blueprint.route("/display/uncompressed/<int:id>/<string:name>")
@login_required
@celery.task
def display_uncompressed_id(id: int, name: str):
    # query all compression services
    uncompressed = media_index.query.filter_by(
        id=id, file_name=name, file_compressed=False
    ).first()
    # if not uncompressed:
    #     return """<h1>No compressed images found</h1>  <a href='/compression_service/'>go to index</a>"""
    return render_template(
        "individual_display.html", img=uncompressed, compressed=False
    )


@compression_service_blueprint.route("/sorted/compressed")
@login_required
@celery.task
def sorted_compressed_render():
    # query all compression services
    compressed = media_index.query.filter_by(file_compressed=True).all()
    if not compressed:
        return """<h1>No compressed images found</h1>  <a href='/compression_service/'>go to index</a>"""
    return render_template("grouped_rendering.html", img=compressed, compressed=True)


@compression_service_blueprint.route("/sorted/uncompressed")
@login_required
@celery.task
def sorted_uncompressed_render():
    # query all compression services
    uncompressed = media_index.query.filter_by(file_compressed=False).all()
    if not uncompressed:
        return """<h1>No compressed images found</h1>  <a href='/compression_service/'>go to index</a>"""
    return render_template("grouped_rendering.html", img=uncompressed, compressed=False)


@compression_service_blueprint.route("/delete/<int:id>/<string:name>")
@login_required
@celery.task
def delete_id(id: int, name: str):
    # query all compression services
    compressed = media_index.query.filter_by(id=id, file_name=name).first()
    if not compressed:
        return """<h1>No compressed images found</h1>  <a href='/compression_service/'>go to index</a>"""
    # delete the image from the file storage
    os.remove(os.path.join(compressed.file_path, compressed.file_name))
    # delete the image from the database
    db.session.delete(compressed)
    db.session.commit()
    return redirect(url_for("compression_service.index_design"))


@compression_service_blueprint.route("/upload", methods=["POST", "GET"])
@login_required
@celery.task
def upload() -> Response:
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
        return redirect(url_for("compression_service.index_design"))
    else:
        return render_template("upload_template.html")


@compression_service_blueprint.route("/existing_compression/<int:id>/<string:name>")
@login_required
@celery.task
def compress_uploaded(id: int, name: str) -> Response:
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


@compression_service_blueprint.route("/compression_upload", methods=["POST", "GET"])
@login_required
@celery.task
def compression_upload() -> Response:
    if request.method == "POST":
        file = request.files["file"]
        file_name = secure_filename(file.filename)
        file_path_static: str = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\static\imgs"))
            + str(rf"\{file_name}")
        )
        file_path_compressed: str = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
            + str(rf"\{file_name}")
        )
        try:
            file.save(file_path_static)
            picture: Image = Image.open(file_path_static)
            picture.save(file_path_compressed, "JPEG", optimize=True, quality=85)
        except OSError as e:
            print(e)
        finally:
            picture: Image = Image.open(file_path_static)
            rgb_im = picture.convert("RGB")
            rgb_im.save(file_path_compressed, "JPEG", optimize=True, quality=85)
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
        return redirect(url_for("compression_service.index_design"))
    else:
        return render_template("upload_template.html")


from .video_compression import views
