import requests
import requests_file
from flask import Blueprint, Response, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.utils import secure_filename

from ..extension_globals.celery import celery
from ..extension_globals.database import db
from ..utils.file_info_utils import allowed_file
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


@video_compression_blueprint.route("/upload/video", methods=["POST"])
@celery.task
def upload_video() -> Response:
    if request.method == "POST":
        try:
            if request.files:
                video_file = request.files["file"]
                if video_file.filename == "":
                    raise BadRequest("No file selected")
                if not allowed_file(video_file.filename):
                    raise BadRequest("File type not allowed")
                _ = assemble_record(video_file, compressing=False, compressed=False)

                db.session.add(_)
                db.session.commit()
                # post the video to storage_sequencer/upload/file
                ipfs_upload_task = celery.send_task(
                    "storage_sequencer.upload_file",
                    kwargs={"file": video_file},
                )
                return Response(
                    f"{ipfs_upload_task.id}", status=200, mimetype="text/plain"
                )
        except BadRequest as e:
            return Response(str(e), status=400, mimetype="text/plain")


@video_compression_blueprint.route("/compress/video", methods=["GET", "POST"])
@celery.task
def compress_video() -> Response:
    if request.method == "POST":
        if request.files:
            try:
                video_file: "ImmutableMultiDict[str, FileStorage]" = request.files[
                    "file"
                ]
            except KeyError:
                if request.form:
                    video_file = request.form["file"]
                if not video_file:
                    return redirect(url_for("video_compression.compress_video")), 302
                else:
                    return redirect(url_for("video_compression.compress_video")), 400

            # _ = assemble_record.apply_async(args=(video_file, True, False))
            # db.session.add(_)
            # db.session.commit()
            requests.post(
                headers={"Content-Type": "multipart/form-data"},
                url="http://localhost:5000/storage/upload/",
                files={"file": video_file},
            )

            return Response(
                "Video compressed successfully",
                status=200,
                mimetype="text/plain",
            )
        return redirect(url_for("video_compression.compress_video")), 302
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
    try:
        video_query = video_media.query.filter_by(id=id, name=name).first()
        return render_template("video_player.html", video_query=video_query)
    except AttributeError:
        if not video_query:
            return redirect(url_for("index_endpoint.index_design")), 400
        else:
            return render_template(
                "video_player.html", video_query=ValueError("Video not found")
            )


@video_compression_blueprint.route(
    "/delete/<int:id>/<string:name>", methods=["GET", "POST"]
)
@login_required
def delete_video(id: int, name: str) -> Response:
    try:
        video_query: video_media = video_media.query.filter_by(id=id, name=name).first()
        db.session.delete(video_query)
        db.session.commit()
        return redirect(url_for("index_endpoint.index_design")), 200
    except AttributeError:
        if not video_query:
            return redirect(url_for("index_endpoint.index_design")), 400
        else:
            return render_template(
                "video_player.html", video_query=ValueError("Video not found")
            )
