import base64
import datetime
import hashlib
import os
import pathlib

import sqlalchemy
from flask import Blueprint

image_compression_blueprint = Blueprint(
    "image_compression",
    __name__,
    template_folder="templates",
    url_prefix="/image_compression",
    static_folder="static/imgs",
)
