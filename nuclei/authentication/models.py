from ..extension_globals.database import db
from ..extension_globals.praetorian import *


class User_Auth(UserMixin,db.Model):
    __tablename__ = "user_auth"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    hashed_password = db.Column(db.String(), nullable=False)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    is_authenticated = False
    is_active = False
    is_anonymous = False

    def __init__(self, email, username, hashed_password):
        self.email = email
        self.username = username
        self.hashed_password = guard.hash_password(hashed_password)

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active

db.create_all()