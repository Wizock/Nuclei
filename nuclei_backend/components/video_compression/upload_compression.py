import logging
import pathlib

import requests
from flask import Response, redirect, render_template, request, url_for
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.utils import secure_filename

from ...extension_globals.celery import celery
from ...extension_globals.database import db
from ...extension_globals.redis import redis_client
from ..storage_sequencer.file_info_utils import allowed_file
from .assemble_records import assemble_record
from .main import video_compression_blueprint


@video_compression_blueprint.route("/upload/video", methods=["POST"])
@celery.task(
    bind=True, name="upload_video", max_retries=3, interval_start=0, interval_step=0.5
)
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
    logging.info("compress_video")
    if request.method == "POST":
        if request.files:
            logging.info(" post request")
            video_files = request.files.getlist("files")
            logging.info(f"{video_files}")
            for video_file in video_files:

                logging.info(f"video_file: {video_file}")

                if redis_client.get(video_file.filename):
                    logging.info("checking redis")

                logging.info("video_file acceptence")

                redis_client.set(video_file.filename, "True")  #
                _ = assemble_record(video_file, True, True)

                db.session.add(_)
                db.session.commit()
                logging.info("try")

                # post the video
                req_comp = requests.post(
                    url_for("storage_sequencer.ipfs_upload"),
                    files={
                        "files": open(
                            pathlib.Path(__file__).parent.absolute()
                            / f"static/compressed/{secure_filename(video_file.filename)}",
                            "rb",
                        )
                    },
                )
            return Response(
                "Video compressed successfully",
                status=200,
                mimetype="text/plain",
            )
        return redirect(url_for("video_compression.compress_video")), 302
