from werkzeug.security import check_password_hash, generate_password_hash

from app.db.repositories.base import BaseRepository
from app.users.models import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

    def login(self, email: str, password: str):
        user = self._model.query.filter_by(email=email).first()
        print(12313, user)
        if user is not None:
            if check_password_hash(user.password, password):
                return user

    def register(self, **data):
        data['password'] = generate_password_hash(data['password'])
        user = super().create(**data)
        return user
