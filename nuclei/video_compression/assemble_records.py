import base64
import datetime
import hashlib
import os
import pathlib
from typing import List

from flask_sqlalchemy import SQLAlchemy

from ..extension_globals.database import db
from .compression_preset import compression_main
from .models import video_media


def assemble_record(
    video_file: "ImmutableMultiDict[str, FileStorage]",
    compressing=False,
    compressed=False,
) -> video_media:
    """
    This function takes a file and returns a video_media object

    :param video_file: the file to be compressed
    :param compressing: whether or not the file is being compressed
    :param compressed: whether or not the file is compressed
    :return: a video_media object
    """

    video_name = video_file.filename
    if (
        video_name.endswith(".mpeg")
        or video_name.endswith(".avi")
        or video_name.endswith(".mp4")
    ):

        file_path: str = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\video_compression\static\videos"))
            + str(rf"\{video_name}")
        )
        file_path_compressed: str = (
            str(pathlib.Path.cwd())
            + str(pathlib.Path(r"\nuclei\video_compression\static\compressed"))
            + str(rf"\{video_name}")
        )
        if not file_path or not file_path_compressed:
            raise OSError("File path is not valid")

        if not compressing:
            video_file.save(file_path)
            file_size_original = os.path.getsize(file_path)
            if file_size_original > (10**10):
                raise OSError("File too large")

            if compressed:
                file_size_compressed = os.path.getsize(file_path)
            file_size_compressed: int = 0
            # get file hash

            file_hash_md5: str = hashlib.md5(open(file_path, "rb").read()).hexdigest()
            if not file_hash_md5:
                raise ValueError("File hash is empty")
            # get file base64
            file_base64: str = base64.b64encode(open(file_path, "rb").read()).decode(
                "utf-8"
            )
            if not file_base64:
                raise ValueError("File base64 is empty")
            # get file extension
            file_extension: str = os.path.splitext(file_path)[1]
            if not file_extension:
                raise ValueError("File extension is empty")
            # get file path
            file_path: str = os.path.dirname(file_path)
            if not file_path:
                raise ValueError("File path is empty")
            # create new CompressionService object
            try:
                compression_service: video_media = video_media(
                    name=video_name,
                    file_path=file_path,
                    file_name=video_name,
                    file_extension=file_extension,
                    file_size_original=file_size_original,
                    file_size_compressed=file_size_compressed,
                    file_hash_md5=file_hash_md5,
                    file_base64=file_base64,
                    file_compressed=compressed,
                    date_created=datetime.datetime.now(),
                    date_updated=datetime.datetime.now(),
                )
            except SQLAlchemy.exc.IntegrityError:
                raise ValueError("File already exists")
            finally:
                return compression_service
        else:
            try:
                video_file.save(file_path)
            except OSError:
                raise OSError("File path is not valid")
            try:
                compression_main(file_path, file_path_compressed, preset="perfect")
            except OSError:
                raise OSError("File path is not valid")

            file_size_original = os.path.getsize(file_path)
            if file_size_original > (10**10):
                raise OSError("File too large")
            file_size_compressed: int = os.path.getsize(file_path_compressed)
            if not file_size_compressed:
                raise ValueError("File size is empty")
            # get file hash
            file_hash_md5: str = hashlib.md5(
                open(file_path_compressed, "rb").read()
            ).hexdigest()
            if not file_hash_md5:
                raise ValueError("File hash is empty")
            # get file base64
            file_base64: str = base64.b64encode(
                open(file_path_compressed, "rb").read()
            ).decode("utf-8")
            if not file_base64:
                raise ValueError("File base64 is empty")
            # get file extension
            file_extension: str = os.path.splitext(file_path_compressed)[1]
            if not file_extension:
                raise ValueError("File extension is empty")
            # get file path
            file_path: str = os.path.dirname(file_path_compressed)
            if not file_path:
                raise ValueError("File path is empty")
            # create new CompressionService object
            try:
                compression_service: video_media = video_media(
                    name=video_name,
                    file_path=file_path,
                    file_name=video_name,
                    file_extension=file_extension,
                    file_size_original=file_size_original,
                    file_size_compressed=file_size_compressed,
                    file_hash_md5=file_hash_md5,
                    file_base64=file_base64,
                    file_compressed=compressed,
                    date_created=datetime.datetime.now(),
                    date_updated=datetime.datetime.now(),
                )
            except SQLAlchemy.exc.IntegrityError:
                raise ValueError("File already exists")
            return compression_service
