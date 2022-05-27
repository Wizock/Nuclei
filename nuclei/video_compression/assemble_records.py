import base64
import datetime
import hashlib
import os
import pathlib
from typing import List
from ..extension_globals.database import db
from .models import video_media
from .compression_preset import compression_main


def assemble_record(
    video_file: "ImmutableMultiDict[str, FileStorage]",
    compressing=False,
    compressed=False,
) -> video_media:

    video_name = video_file.filename

    file_path: str = (
        str(pathlib.Path.cwd())
        + str(pathlib.Path(r"\nuclei\compression_service\static\videos"))
        + str(rf"\{video_name}")
    )
    file_path_compressed: str = (
        str(pathlib.Path.cwd())
        + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
        + str(rf"\{video_name}")
    )

    if not compressing:
        video_file.save(file_path)
        file_size_original = os.path.getsize(file_path)
        if compressed:
            file_size_compressed = os.path.getsize(file_path)
        file_size_compressed: int = 0
        # get file hash
        file_hash_md5: str = hashlib.md5(open(file_path, "rb").read()).hexdigest()
        # get file base64
        file_base64: str = base64.b64encode(open(file_path, "rb").read()).decode(
            "utf-8"
        )
        # get file extension
        file_extension: str = os.path.splitext(file_path)[1]
        # get file path
        file_path: str = os.path.dirname(file_path)
        # create new CompressionService object
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
        print(compression_service)
        return compression_service
    else:
        video_file.save(file_path)
        print("video is saved")
        compression_main(file_path, file_path_compressed, preset="perfect")
        print("video was compressed")
        file_size_original = os.path.getsize(file_path)
        file_size_compressed: int = os.path.getsize(file_path_compressed)
        # get file hash
        file_hash_md5: str = hashlib.md5(
            open(file_path_compressed, "rb").read()
        ).hexdigest()
        # get file base64
        file_base64: str = base64.b64encode(
            open(file_path_compressed, "rb").read()
        ).decode("utf-8")
        # get file extension
        file_extension: str = os.path.splitext(file_path_compressed)[1]
        # get file path
        file_path: str = os.path.dirname(file_path_compressed)
        # create new CompressionService object
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
        print(compression_service)
        return compression_service
