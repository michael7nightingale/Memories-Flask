import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __repr__(self):
        return f"{self.id=}, {self.username=}"


class Themes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    isPublic = db.Column(db.Boolean)
    key = db.Column(db.String(80), nullable=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"{self.id=}, {self.title=}"


class TextCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ask_side = db.Column(db.Text)
    image = db.Column(db.LargeBinary, nullable=True)
    answer_side = db.Column(db.String(255))
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))

    def __repr__(self):
        return f"{self.id=}, {self.ask_side=}"



