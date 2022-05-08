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
    # date created
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    # date updated
    date_created = db.Column(
        db.DateTime, nullable=True, default=db.func.now(), onupdate=db.func.now()
    )

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
        date_created: str = "",
        date_updated: str = "",
    ) -> None:
        self.name: str = name
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.file_extension: str = file_extension
        self.file_size: int = file_size
        self.file_hash_md5: str = file_hash_md5
        self.file_base64: str = file_base64
        self.file_compressed: bool = file_compressed
        self.date_created: str = date_created
        self.date_updated: str = date_updated


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
    # date created
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    # date updated
    date_created = db.Column(
        db.DateTime, nullable=True, default=db.func.now(), onupdate=db.func.now()
    )

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
        date_created: str = "",
        date_updated: str = "",
    ) -> None:
        self.name: str = name
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.file_extension: str = file_extension
        self.file_size: int = file_size
        self.file_hash_md5: str = file_hash_md5
        self.file_base64: str = file_base64
        self.file_compressed: bool = file_compressed
        self.date_created: str = date_created
        self.date_updated: str = date_updated


db.create_all()
