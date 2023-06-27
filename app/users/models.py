import flask_login
from uuid import uuid4

from app.extensions import db


class User(db.Model, flask_login.UserMixin):    # type: ignore
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.id=}, {self.username=}"
