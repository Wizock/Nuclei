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


@file_compression.route("/compress", methods=["POST"])
def compress_misc_file() -> Response:
    """
    This function takes a file and returns a video_media object
    """

    file_to_compress = request.files["file"]

    input_data = open("1.png", "rb").read()

    compressed = lz4.frame.compress(
        input_data,
        compression_level=lz4.frame.COMPRESSIONLEVEL_MAX,
        block_size=lz4.frame.BLOCKSIZE_MAX1MB,
        block_linked=True,
        content_checksum=True,
    )
    with open("compressed_data.lz4", "wb") as fout:
        fout.write(compressed)

    print(compressed)


@file_compression.route("/decompress", methods=["POST"])
def decompress_misc_file() -> Response:

    fin = open("compressed_data.lz4", "rb").read()

    decompressed = lz4.frame.decompress(fin)
