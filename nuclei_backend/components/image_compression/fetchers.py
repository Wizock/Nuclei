import os

from flask import Response, redirect, url_for

from ...extension_globals.celery import celery
from ...extension_globals.database import db
from .main import compression_service_blueprint
from .models import media_index


@compression_service_blueprint.route("/delete/<int:id>/<string:name>")
@celery.task
def delete_id(id: int, name: str) -> Response:
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
