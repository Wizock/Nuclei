import base64
import datetime
import hashlib
import os
import pathlib

from PIL import Image
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from werkzeug.utils import secure_filename

from .image_helpers import handle_image_incompatibilities
from .models import media_index


def assemble_image_record(
    image_file: FileStorage,
    compressing: bool = False,
):
    file_name = secure_filename(image_file.filename)
    file_path_static: str = (
        str(pathlib.Path.cwd())
        + str(pathlib.Path(r"\nuclei\compression_service\static\imgs"))
        + str(rf"\{file_name}")
    )
    file_path_compressed: str = (
        str(pathlib.Path.cwd())
        + str(pathlib.Path(r"\nuclei\compression_service\static\compressed"))
        + str(rf"\{file_name}")
    )
    if compressing:
        try:
            image_file.save(file_path_static)
            picture: Image = Image.open(file_path_static)
            picture.save(file_path_compressed, "JPEG", optimize=True, quality=85)
            handle_image_incompatibilities(
                picture,
                picture.format,
                os.path.getsize(file_path_static),
                picture.width,
                picture.height,
                picture.mode,
            )
        except OSError as e:
            print(e)
        finally:
            picture: Image = Image.open(file_path_static)
            rgb_im = picture.convert("RGB")
            rgb_im.save(file_path_compressed, "JPEG", optimize=True, quality=85)
        file_size_original = os.path.getsize(file_path_static)
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
        compression_service: media_index = media_index(
            name=file_name,
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            file_size_original=file_size_original,
            file_size_compressed=file_size_compressed,
            file_hash_md5=file_hash_md5,
            file_base64=file_base64,
            file_compressed=True,
            date_created=datetime.datetime.now(),
            date_updated=datetime.datetime.now(),
        )
        return compression_service
    try:
        image_file.save(file_path_static)
        # get file size
        file_size = os.path.getsize(file_path_static)
        # get file hash
        file_hash_md5 = hashlib.md5(open(file_path_static, "rb").read()).hexdigest()
        # get file base64
        file_base64 = base64.b64encode(open(file_path_static, "rb").read()).decode(
            "utf-8"
        )
        file_size_original = os.path.getsize(file_path_static)
        # get file extension
        file_extension = os.path.splitext(file_path_static)[1]
        # get file path
        file_path = os.path.dirname(file_path_static)
        # create new CompressionService object
        compression_service = media_index(
            name=file_name,
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            file_size_original=file_size_original,
            file_size_compressed=0,
            file_hash_md5=file_hash_md5,
            file_base64=file_base64,
            file_compressed=False,
            date_created=datetime.datetime.now(),
            date_updated=datetime.datetime.now(),
        )
    except OSError as e:
        return e

    except (IntegrityError or OperationalError or ProgrammingError) as e:
        return e

    return compression_service
