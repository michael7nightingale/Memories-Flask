from app.extensions import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ask_side = db.Column(db.Text)
    image = db.Column(db.LargeBinary, nullable=True)
    answer_side = db.Column(db.String(255))
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'))

    def __repr__(self):
        return f"{self.id=}, {self.ask_side=}"


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    isPublic = db.Column(db.Boolean)
    key = db.Column(db.String(80), nullable=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.id=}, {self.title=}"
