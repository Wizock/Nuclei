import requests
import sqlalchemy
from flask import (Blueprint, Response, redirect, render_template, request,
                   url_for)

storage_sequencer_controller = Blueprint(
    "storage_sequencer",
    __name__,
    template_folder="templates",
    url_prefix="/storage",
    static_folder="static/imgs",
)

from ..extension_globals.celery import celery
from ..extension_globals.database import db
from .config import storage_sequence_config
from .model import file_tracker

storage_sequencer_controller.config = storage_sequence_config

from .download import *
from .upload import *
