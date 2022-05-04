from nuclei import __libraries__

db = __libraries__.return_db()


class CompressionService(db.Model):
    __tablename__ = "compression_service"
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

    def __init__(
        self,
        name,
        file_path,
        file_name,
        file_extension,
        file_size,
        file_hash_md5="",
        file_base64="",
    ) -> None:
        self.name = name
        self.file_path = file_path
        self.file_name = file_name
        self.file_extension = file_extension
        self.file_size = file_size
        self.file_hash_md5 = file_hash_md5
        self.file_base64 = file_base64
