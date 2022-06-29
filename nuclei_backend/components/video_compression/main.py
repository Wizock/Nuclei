from flask import Blueprint

video_compression_blueprint = Blueprint(
    "video_compression",
    __name__,
    template_folder="templates",
    url_prefix="/video_compression",
    static_folder="static/compressed",
)

from .fetchers import *
from .upload_compression import *  # noqa: F401,F403
