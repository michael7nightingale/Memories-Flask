from sqlalchemy import Table
from app.extensions import db


class BaseRepository:

    def __init__(self, model):
        self._model = model

    def get(self, id_: int):
        return self._model.query.get(id_)

    def filter_by(self, **kwargs) -> list:
        return self._model.query.filter_by(**kwargs).all()

    def all(self) -> list:
        return self._model.query.all()

    def create(self, **kwargs):
        instance = self._model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def delete(self, id_) -> None:
        theme = self._model.query.get(id_)
        db.session.delete(theme)
        db.session.commit()

    def get_by(self, **kwargs):
        return self._model.query.filter_by(**kwargs).first()
