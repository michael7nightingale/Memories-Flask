from typing import Any, List

from app.db.repositories.base import BaseRepository
from .models import Theme, Card
from ..extensions import db


class ThemeRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Theme)

    def all_by_user(self, user_id: str) -> List[Any]:
        return super().filter_by(user_id=user_id)

    def find(self, string: str) -> List[Any]:
        public_themes = self._model.query.filter_by(isPublic=True)
        return public_themes.filter(self._model.title.contains(string)).all()  # type: ignore


class CardRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Card)

    def all_by_theme(self, theme_id: str) -> List[Any]:
        return super().filter_by(theme_id=theme_id)

    def count_by_theme(self, theme_id: str) -> int:
        len_cards = self._model.query.filter_by(theme_id=theme_id).count()  # type: ignore
        return len_cards    # type: ignore

    def delete_by_theme(self, theme_id: str) -> None:
        cards = super().filter_by(theme_id=theme_id)
        db.session.delete(cards)
        db.session.commit()
