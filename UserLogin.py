"""METHODS` NAMES ARE VERY IMPORTANT. DO NOT CHANGE"""


class UserLogin:
    """Class for managing user sessions"""
    __user: None

    def fromDB(self, user_id, dbase):
        self.__user = dbase.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return False

    def is_anonymous(self):
        return

    def is_active(self):
        return True

    def get_id(self):
        return self.__user['id']

