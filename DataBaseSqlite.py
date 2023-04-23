import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


class DataBaseManager:
    def __init__(self, self_, db: sqlite3.Connection):
        # self = self_
        self._db = db
        self._cursor = db.cursor()


class UsersMixin(DataBaseManager):
    def getUser(self, user_id):
        """Check if user in the table"""
        try:
            self._cursor.execute("SELECT * from users WHERE id = ? LIMIT 1", (user_id, ))
            res = self._cursor.fetchone()
            if not res:
                print('User is not found')
                return False
            return res
        except sqlite3.Error as e:
            print(f"Error while registering user: {e}")
            return False

    def getUserByEmail(self, email):
        """Get single user by email"""
        try:
            self._cursor.execute("SELECT * FROM users WHERE email = ? LIMIT 1", (email, ))
            res = self._cursor.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД")
        return False

    def getUsers(self):
        """Get all users from the table"""
        try:
            self._cursor.execute("""SELECT * FROM users""")
            res = self._cursor.fetchall()
            if res:
                return res
        except ConnectionError:
            print("Error while select * from users")
        return []

    def registerUser(self, username, email, password):
        """Create user"""
        try:
            self._cursor.execute(f"SELECT email FROM users")
            res = self._cursor.fetchall()
            amount = [i[0] for i in res]
            if email in amount:
                print("Пользователь с такои email уже существует")
                return False
            self._cursor.execute(f"INSERT INTO users VALUES(NULL, ?, ?, ?)", (username, password, email))
            self._db.commit()
        except sqlite3.Error as e:
            print(f"Error while registering user: {e}")
            return False

        return True


class CardsMixin(DataBaseManager):
    def getCardsByUser(self, user_id):
        try:
            self._cursor.execute("SELECT * from cards WHERE user_id = ? LIMIT 50", (user_id, ))
            cards = self._cursor.fetchall()
            return cards
        except sqlite3.Error as e:
            print("Ошибка при получении карт из БД:" + str(e))


class ThemesMixin(DataBaseManager):
    pass


class DataBase(UsersMixin, CardsMixin, ThemesMixin):
    """Class for managing database for whole app"""

    def __init__(self, db: sqlite3.Connection):
        self._db = db
        self._cursor = db.cursor()







