from __future__ import annotations

from argparse import FileType
from ast import Bytes
from ctypes.wintypes import BOOL, INT
from datetime import date
from email.charset import BASE64
from hashlib import md5
from pathlib import Path
from typing import *

from sqlalchemy import DATE
from typing_extensions import *

from ..extension_globals.database import db


class media_index(db.Model):
    __tablename__ = "media_index"

    id: INT = db.Column(db.Integer(), primary_key=True)
    name: LiteralString = db.Column(db.String(255), nullable=False)
    # file path
    file_path: Path = db.Column(db.String(255), nullable=False)
    # file name
    file_name: LiteralString = db.Column(db.String(255), nullable=False)
    # file extension
    file_extension: FileType = db.Column(db.String(255), nullable=False)
    # file size original
    file_size_original: INT = db.Column(db.Integer(), nullable=False)
    # file size compressed
    file_size_compressed: Bytes = db.Column(db.Integer(), nullable=False)
    # file hash
    file_hash_md5: md5 = db.Column(db.String(255), nullable=True, unique=True)
    # file base64
    file_base64: BASE64 = db.Column(db.String(255), nullable=True)
    # file compressed bool
    file_compressed: BOOL = db.Column(db.Boolean(), nullable=False)
    # date created
    date_created: DATE = db.Column(db.DateTime, nullable=False, default=db.func.now())
    # date updated
    date_created: DATE = db.Column(
        db.DateTime, nullable=True, default=db.func.now(), onupdate=db.func.now()
    )

    def __init__(
        self,
        name: str = "",
        file_path: str = "",
        file_name: str = "",
        file_extension: str = "",
        file_size_original: int = 0,
        file_size_compressed: int = 0,
        file_hash_md5: str = "",
        file_base64: str = "",
        file_compressed: bool = False,
        date_created: str = "",
        date_updated: str = "",
    ) -> None:
        """

        Initialize the media_index class.

        :param name: name of the file
        :param file_path: path of the file
        :param file_name: name of the file
        :param file_extension: extension of the file
        :param file_size: size of the file
        :param file_hash_md5: md5 hash of the file
        :param file_base64: base64 of the file
        :param file_compressed: bool if file is compressed
        :param date_created: date created
        :param date_updated: date updated

        """
        self.name: str = name
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.file_extension: str = file_extension
        self.file_size_original: int = file_size_original
        self.file_size_compressed: int = file_size_compressed
        self.file_hash_md5: str = file_hash_md5
        self.file_base64: str = file_base64
        self.file_compressed: bool = file_compressed
        self.date_created: str = date_created
        self.date_updated: str = date_updated


db.create_all()
