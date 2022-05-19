from flask import redirect, render_template, request
from flask_login import login_required

from ...extension_globals.celery import celery
from ...extension_globals.database import db
from ..models import media_index
from ..views import compression_service_blueprint
from .assemble_records import assemble_record
from .compression_preset import compression_main


@compression_service_blueprint.route("/upload/video", methods=["GET", "POST"])
@login_required
@celery.task
def upload_video():
    if request.method == "POST":
        if request.files:
            video_file = request.files["file"]
            _ = assemble_record(video_file, compressing=False, compressed=False)
            db.session.add(_)
            db.session.commit()

    return render_template("upload_template.html")


@compression_service_blueprint.route("/compress/video", methods=["GET", "POST"])
@login_required
@celery.task
def compress_video():
    if request.method == "POST":
        print("you posted")
        if request.files:
            video_file = request.files["file"]
            _ = assemble_record(video_file, compressing=True, compressed=True)
            db.session.add(_)
            db.session.commit()
            return redirect("/compression_service/")
    else:
        return render_template("upload_template.html")


@compression_service_blueprint.route("/compressed/video", methods=["GET"])
def compressed_video():
    return render_template("compression_service/compressed_video.html")
