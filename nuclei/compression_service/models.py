import os

from ..extension_globals.database import db


class media_index(db.Model):
    __tablename__ = "media_index"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # file path
    file_path = db.Column(db.String(255), nullable=False)
    # file name
    file_name = db.Column(db.String(255), nullable=False)
    # file extension
    file_extension = db.Column(db.String(255), nullable=False)
    # file size
    file_size = db.Column(db.Integer(), nullable=False)
    # file hash
    file_hash_md5 = db.Column(db.String(255), nullable=True)
    # file base64
    file_base64 = db.Column(db.String(255), nullable=True)
    # file compressed bool
    file_compressed = db.Column(db.Boolean(), nullable=False)

    def __init__(
        self,
        name: str = "",
        file_path: str = "",
        file_name: str = "",
        file_extension: str = "",
        file_size: int = 0,
        file_hash_md5: str = "",
        file_base64: str = "",
        file_compressed: bool = False,
    ) -> None:
        self.name: str = name
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.file_extension: str = file_extension
        self.file_size: int = file_size
        self.file_hash_md5: str = file_hash_md5
        self.file_base64: str = file_base64
        self.file_compressed: bool = file_compressed


class compression_index(db.Model):
    __tablename__ = "compression_index"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # file path
    file_path = db.Column(db.String(255), nullable=False)
    # file name
    file_name = db.Column(db.String(255), nullable=False)
    # file extension
    file_extension = db.Column(db.String(255), nullable=False)
    # file size
    file_size = db.Column(db.Integer(), nullable=False)
    # file hash
    file_hash_md5 = db.Column(db.String(255), nullable=True)
    # file base64
    file_base64 = db.Column(db.String(255), nullable=True)
    # file compressed bool
    file_compressed = db.Column(db.Boolean(), nullable=False)

    def __init__(
        self,
        name: str = "",
        file_path: str = "",
        file_name: str = "",
        file_extension: str = "",
        file_size: int = 0,
        file_hash_md5: str = "",
        file_base64: str = "",
        file_compressed: bool = False,
    ) -> None:
        self.name: str = name
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.file_extension: str = file_extension
        self.file_size: int = file_size
        self.file_hash_md5: str = file_hash_md5
        self.file_base64: str = file_base64
        self.file_compressed: bool = file_compressed


db.create_all()
