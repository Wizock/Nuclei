import base64
import datetime
import hashlib
import os
import pathlib

import sqlalchemy
from flask import Blueprint, Response, redirect, render_template, request, url_for

# import login required decorator
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from werkzeug.utils import secure_filename

compression_service_blueprint = Blueprint(
    "compression_service",
    __name__,
    template_folder="templates",
    url_prefix="/compression_service",
    static_folder="static/imgs",
)

from ...extension_globals.celery import celery
from ...extension_globals.database import db
from .image_helpers import handle_image_incompatibilities
from .models import media_index
