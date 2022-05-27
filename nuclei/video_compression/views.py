from flask import Blueprint, Response, redirect, render_template, request, url_for
from flask_login import login_required

from ..compression_service.models import media_index
from ..extension_globals.celery import celery
from ..extension_globals.database import db
from .assemble_records import assemble_record
from .compression_preset import compression_main

video_compression_blueprint = Blueprint(
    "video_compression",
    __name__,
    template_folder="templates",
    url_prefix="/video_compression",
    static_folder="static/",
)

from ..extension_globals.celery import celery
from ..extension_globals.database import db


@video_compression_blueprint.route("/upload/video", methods=["GET", "POST"])
@login_required
@celery.task
def upload_video() -> Response:
    if request.method == "POST":
        if request.files:
            video_file = request.files["file"]
            _ = assemble_record(video_file, compressing=False, compressed=False)
            db.session.add(_)
            db.session.commit()
    return render_template("upload_template.html")


@video_compression_blueprint.route("/compress/video", methods=["GET", "POST"])
@login_required
@celery.task
def compress_video() -> Response:
    if request.method == "POST":
        print("you posted")
        if request.files:
            video_file = request.files["file"]
            _ = assemble_record(video_file, compressing=True, compressed=True)
            db.session.add(_)
            db.session.commit()
            return redirect("/compression_service/")
    else:
        return render_template(
            "upload_template.html",
            loading=url_for("compression_service.static", filename="loading.gif"),
        )


@video_compression_blueprint.route("/compressed/video", methods=["GET"])
def compressed_video():
    return render_template("compression_service/compressed_video.html")
