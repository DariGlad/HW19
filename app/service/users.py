import base64
import hashlib
import hmac

from app.helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UsersService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        """ Возвращает данные всех пользователей """

        return self.dao.get_all()

    def get_one(self, user_id):
        """ Возвращает данные по id пользователя """

        return self.dao.get_one(user_id)

    def get_by_username(self, username):
        """ Поиск по имени пользователя """
        return self.dao.get_by_username(username)

    def check_is_dict(self, data):
        """ Проверяем, являются ли данные словарём """

        return self.dao.check_is_dict(data)

    def create(self, data):
        """ Создание данных нового пользователя """

        data["password"] = self.get_hash(data["password"])
        return self.dao.create(data)

    def update(self, user_id, data):
        """ Обновление данных пользователя по id """

        user = self.get_one(user_id)
        user.id = data.get("id")
        user.username = data.get("username")
        user.password = self.get_hash(data.get("password"))
        user.role = data.get("role")

        return self.dao.update(user)

    def update_partial(self, user_id, data):
        """ Частичное обновление данных пользователя по id """

        user = self.get_one(user_id)
        if "id" in data:
            user.id = data.get("id")
        if "username" in data:
            user.username = data.get("username")
        if "password" in data:
            user.password = self.get_hash(data.get("password"))
        if "role" in data:
            user.role = data.get("role")
        return self.dao.update(user)

    def delete(self, user_id):
        """ Удаление данных пользователя по id """

        self.dao.delete(user_id)

    def get_hash(self, password):
        """ Метод хеширования пароля """

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(password_hash)

    def compare_passwords(self, password_hash, password):
        """ Метод проверки хеширования паролей на идентичность(совпадение) """
        decoded_digest = base64.b64decode(password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)
