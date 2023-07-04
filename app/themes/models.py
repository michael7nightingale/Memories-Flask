from uuid import uuid4

from app.extensions import db


class Card(db.Model):   # type: ignore
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid4()))
    question = db.Column(db.Text)
    answer = db.Column(db.String(255))
    image = db.Column(db.String, nullable=True)
    theme_id = db.Column(db.String(50), db.ForeignKey('theme.id'))

    def __repr__(self):
        return f"{self.id=}, {self.ask_side=}"


class Theme(db.Model):  # type: ignore
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(80))
    isPublic = db.Column(db.Boolean, default=True)
    key = db.Column(db.String(100), nullable=True, unique=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.id=}, {self.title=}"
