import flask_login
from uuid import uuid4

from app.extensions import db


class UserMixin(flask_login.UserMixin):
    @property
    def is_active(self):
        return self._is_active


class User(db.Model, UserMixin):    # type: ignore
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    _is_active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.id=}, {self.username=}"
