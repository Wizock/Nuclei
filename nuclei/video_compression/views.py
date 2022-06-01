from flask import Blueprint, Response, redirect, render_template, request, url_for
from flask_login import login_required

from ..extension_globals.celery import celery
from ..extension_globals.database import db
from .assemble_records import assemble_record
from .compression_preset import compression_main
from .models import video_media

video_compression_blueprint = Blueprint(
    "video_compression",
    __name__,
    template_folder="templates",
    url_prefix="/video_compression",
    static_folder="static/compressed",
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
            return Response(
                "Video file uploaded successfully",
                status=200,
                mimetype="text/plain",
            )
        return Response(
            "No file was uploaded",
            status=400,
            mimetype="text/plain",
        )
    return render_template("upload_template.html"), 200


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
            return redirect("/")
    else:
        return render_template(
            "upload_template.html",
            loading=url_for("compression_service.static", filename="loading.gif"),
        )


@video_compression_blueprint.route(
    "/video/<int:id>/<string:name>", methods=["GET", "POST"]
)
@login_required
def view_video(id: int, name: str) -> Response:
    video_query = video_media.query.filter_by(id=id, name=name).first()
    print(video_query)
    return render_template("video_player.html", video_query=video_query)


@video_compression_blueprint.route(
    "/delete/<int:id>/<string:name>", methods=["GET", "POST"]
)
@login_required
def delete_video(id: int, name: str) -> Response:
    video_query = video_media.query.filter_by(id=id, name=name).first()
    db.session.delete(video_query)
    db.session.commit()
    return redirect("/")
