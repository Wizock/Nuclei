from flask import Blueprint

storage_sequencer_controller = Blueprint(
    "storage_sequencer",
    __name__,
    template_folder="templates",
    url_prefix="/storage",
    static_folder="static/imgs",
)

from .config import storage_sequence_config

storage_sequencer_controller.config = storage_sequence_config

from .download import *
from .upload import *
