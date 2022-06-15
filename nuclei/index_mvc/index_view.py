import base64
import datetime
import hashlib
import os
import pathlib

from flask import Blueprint, Response, abort, render_template, url_for
from flask_cors import cross_origin

# import login required decorator
from flask_login import login_required
import flask_praetorian

_index_view = Blueprint(
    "index_endpoint",
    __name__,
    template_folder="templates",
    url_prefix="/",
)

from ..compression_service.models import media_index
from ..extension_globals.celery import celery
from ..extension_globals.database import db
from ..video_compression.models import video_media


@_index_view.route("/", methods=["GET"])
@cross_origin()
@flask_praetorian.auth_required
def index_design() -> Response:
    # query media models to get all media objects
    images = media_index.query.all()
    videos = video_media.query.all()

    images.sort(key=lambda x: x.date_created)
    videos.sort(key=lambda x: x.date_created)
    # merge the data
    data = images + videos
    data.sort(key=lambda x: x.date_created)

    return Response(
        data,
        mimetype="application/json",
        status=200,
        headers={"Access-Control-Allow-Origin": "*"},
    )
