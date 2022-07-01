from typing import Any

import flask_praetorian
from flask import Blueprint, Response, jsonify
from flask_cors import cross_origin

_index_view = Blueprint(
    "index_endpoint",
    __name__,
    template_folder="templates",
    url_prefix="/",
)
from ..image_compression.models import media_index
from ..video_compression.models import video_media


@_index_view.route("/index", methods=["GET"])
def index_design() -> Response:
    # query media models to get all media objects
    images = media_index.query.all()
    videos = video_media.query.all()

    images.sort(key=lambda x: x.date_created)
    videos.sort(key=lambda x: x.date_created)
    # merge the data
    data = images + videos
    data.sort(key=lambda x: x.date_created)

    media: dict[int, dict[str, Any]] = {
        query.id: {
            "name": query.name,
            "file_path": query.file_path,
            "file_name": query.file_name,
            "file_extension": query.file_extension,
            "file_size_original": query.file_size_original,
            "file_size_compressed": query.file_size_compressed,
            "file_hash_md5": query.file_hash_md5,
            "file_base64": query.file_base64,
            "file_compressed": query.file_compressed,
            "date_created": query.date_created,
            "date_updated": query.date_updated,
        }
        for query in data
    }

    print(media)
    return Response(jsonify(media), mimetype="application/json", status=200)
