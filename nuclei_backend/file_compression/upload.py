import lz4.frame
from lz4.block import compress, decompress
import os
import base64
import datetime
import hashlib
import os
import pathlib
from typing import List
from .main import file_compression
import requests
import requests_file
from flask import Blueprint, Response, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.utils import secure_filename
import gevent
from gevent import *


@file_compression.route("/compress", methods=["POST"])
def compress_misc_file() -> Response:
    """
    This function takes a file and returns a video_media object
    """
    if request.method == "POST":
        file_to_compress = request.files["file"]
        file_name = file_to_compress.filename
        input_data = open(secure_filename(file_to_compress), "rb").read()

        compressed = lz4.frame.compress(
            input_data,
            compression_level=lz4.frame.COMPRESSIONLEVEL_MAX,
            block_size=lz4.frame.BLOCKSIZE_MAX1MB,
            block_linked=True,
            content_checksum=True,
        )
        with open(f"{file_name}.lz4", "wb") as fout:
            fout.write(compressed)

    print(compressed)


@file_compression.route("/decompress", methods=["POST"])
def decompress_misc_file() -> Response:

    fin = open("compressed_data.lz4", "rb").read()

    decompressed = lz4.frame.decompress(fin)
