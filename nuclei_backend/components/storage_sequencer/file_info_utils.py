import typing

from ...extension_globals.database import db
from ..compression_service.models import media_index
from ..video_compression.models import video_media

image_type = typing.Union[str, bytes]
video_type = typing.Union[str, bytes]


def allowed_file(filename: typing.AnyStr) -> bool:
    if "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "png",
        "jpg",
        "jpeg",
    ]:
        # check if the file exists in the media_index table
        if media_index.query.filter_by(file_name=filename).first():
            # return the file with the image type
            return True
    if "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "mp4",
        "mov",
        "avi",
    ]:
        # check if the file exists in the media_index table
        if video_media.query.filter_by(file_name=filename).first():
            # return the file with the image type
            return True


def return_file_path(filename: typing.Callable) -> str:
    if filename == image_type:
        # check if the file exists in the media_index table
        if media_index.query.filter_by(file_name=filename).first():
            return media_index.query.filter_by(file_name=filename).first().file_path
        # check if the file exists in the media_index table
    if filename == video_type:
        video_media.query.filter_by(file_name=filename).first().file_path
        return video_media.query.filter_by(file_name=filename).first().file_path
