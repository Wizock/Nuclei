from ...extension_globals.celery import celery
from ...extension_globals.database import db
from .main import compression_service_blueprint
from .image_helpers import handle_image_incompatibilities
from .models import media_index

import base64
import datetime
import hashlib
import os
import pathlib

import sqlalchemy
from flask import Blueprint, Response, redirect, render_template, request, url_for

# import login required decorator
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from werkzeug.utils import secure_filename


@compression_service_blueprint.route("/delete/<int:id>/<string:name>")
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
    return redirect(url_for("index_endpoint.index_design"))
