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

_index_view = Blueprint(
    "index_view",
    __name__,
    template_folder="templates",
    url_prefix="/",
)

from ..extension_globals.celery import celery
from ..extension_globals.database import db
from ..compression_service.models import media_index
from ..video_compression.models import video_media


@_index_view.route("/")
@_index_view.route("/index_design", methods=["POST", "GET"])
@login_required
def index_design():
    # query media models to get all media objects
    images = media_index.query.all()
    videos = video_media.query.all()

    images.sort(key=lambda x: x.date_created)
    videos.sort(key=lambda x: x.date_created)
    # merge the data
    data = images + videos
    data.sort(key=lambda x: x.date_created)
    # render the index_design template

    return render_template("dashboard.html", data=data)
