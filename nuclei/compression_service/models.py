from nuclei import app

db = app.return_db()

class CompressionService(db.Model):
    __tablename__ = 'compression_service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # file path
    file_path = db.Column(db.String(255), nullable=False)
    # file name
    file_name = db.Column(db.String(255), nullable=False)
    # file extension
    file_extension = db.Column(db.String(255), nullable=False)
    # file size
    file_size = db.Column(db.Integer, nullable=False)
    # file hash
    file_hash_md5 = db.Column(db.String(255), nullable=True)
    # file base64
    file_base64 = db.Column(db.String(255), nullable=True)
    