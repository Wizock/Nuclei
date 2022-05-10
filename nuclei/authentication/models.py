from __future__ import annotations

from typing import *

from flask_login import UserMixin
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing_extensions import *
from werkzeug.security import check_password_hash, generate_password_hash

from ..extension_globals.database import db

BaseModel: DeclarativeMeta = db.Model


class User(UserMixin, BaseModel):
    """
    User model.
    """

    __tablename__ = "user_auth"
    id: int = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    hashed_password = db.Column(db.String(), nullable=False)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    is_authenticated: bool
    is_active: bool
    is_anonymous: bool

    def __init__(
        self,
        email: LiteralString,
        username: LiteralString,
        hashed_password: LiteralString,
    ):
        """
        Initialize a new user.
        :param email: user's email
        :param username: user's username
        :param hashed_password: user's hashed password

        """
        self.email: LiteralString = email
        self.username: LiteralString = username
        self.hashed_password: LiteralString = generate_password_hash(hashed_password)

    def is_active(self) -> bool:
        """
        Check if user is active.
        """
        return self.is_active

    def check_password(self, password) -> bool:
        """
        Check if user's password is correct.
        """
        return check_password_hash(self.hashed_password, password)

    def get_id(self) -> str:
        """
        Get the user's id.
        """
        return self.id

    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated.
        """
        return self.authenticated

    def is_anonymous(self) -> bool:
        """
        Check if user is anonymous.
        """
        return self.is_anonymous

    @property
    def identity(self) -> str:
        """
        Get the user's identity.
        """
        return self.id

    @property
    def rolenames(self) -> list:
        """
        Get the user's roles.
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self) -> str:
        """
        Get the user's password.
        """
        return self.hashed_password

    @classmethod
    def lookup(cls, username) -> "User":
        """
        Lookup a user by username.
        """

        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id) -> "User":
        """
        Lookup a user by id.
        """

        return cls.query.get(id)

    def is_valid(self) -> bool:
        """
        Check if user is valid.
        """
        return self.is_active


db.create_all()
