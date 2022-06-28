from flask import Blueprint

file_compression = Blueprint(
    "file_compression",
    __name__,
    template_folder="templates",
    url_prefix="/misc",
    static_folder="static/imgs",
)


from .download import *
from .upload import *
