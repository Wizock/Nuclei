import base64
import datetime
import hashlib
import os
import pathlib

import sqlalchemy
from flask import Response, redirect, render_template, request, url_for

# import login required decorator
from flask_login import login_required
from PIL import Image
from werkzeug.utils import secure_filename

from nuclei_backend.components.compression_service.assemble_records import (
    assemble_image_record,
)

from ...extension_globals.celery import celery
from ...extension_globals.database import db
from .main import compression_service_blueprint
from .models import media_index


@compression_service_blueprint.route("/upload", methods=["POST", "GET"])
@login_required
@celery.task
def upload() -> Response:
    if request.method == "POST":
        file = request.files["file"]
        # check if the file is an image
        if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            return redirect(url_for("compression_service.upload"))
        # check if the file is a video type
        elif file.content_type in ["video/mp4", "video/mpeg", "video/ogg"]:
            return redirect(url_for("compression_service.upload"))
        # the file must be an unknown type
        if file.filename == "":
            return Response(
                "No file selected",
                status=400,
                mimetype="text/plain",
            )
        if file:

            file_name = secure_filename(file.filename)
            compression_service = assemble_image_record(file_name, False)
            # add new CompressionService object to database
            db.session.add(compression_service)
            # commit changes to database
            db.session.commit()
            return redirect(url_for("index_endpoint.index_design"))
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
@celery.task
def compression_upload() -> Response:
    if request.method == "POST":
        try:
            file = request.files["file"]
        except Exception as e:
            return Response(
                "No file selected",
                status=302,
                mimetype="text/plain",
            )

        if file.filename == "":
            return Response(
                "No file selected",
                status=400,
                mimetype="text/plain",
            )
        if file:
            file_name = secure_filename(file.filename)
            if (
                file_name.endswith(".jpg")
                or file_name.endswith(".png")
                or file_name.endswith(".jpeg")
            ):
                # create new CompressionService object
                try:
                    compression_service = assemble_image_record(file, True)
                    # add new CompressionService object to database
                    db.session.add(compression_service)
                    # commit changes to database
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError as e:
                    return (
                        redirect(f"/compression_service/display/compressed/{e}"),
                        400,
                    )
                return redirect(url_for("index_endpoint.index_design"))
            else:
                return redirect(f"/compression_service/compression_upload"), 400
        else:
            return redirect(f"/compression_service/compression_upload"), 302
    else:
        return render_template("upload_template.html")
