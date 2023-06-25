from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()


def add_instance(model_instance):
    try:
        db.session.add(model_instance)
        db.session.flush()
        db.session.commit()
        return model_instance.id
    except Exception as e:
        print(e)
