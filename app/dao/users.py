from sqlalchemy.exc import IntegrityError

from app.dao.model.user import User


class UsersDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """ Возвращает данные всех пользователей """

        return self.session.query(User).all()

    def get_one(self, user_id):
        """ Возвращает данные по id пользователя, либо ошибку 404 """

        return self.session.query(User).filter(User.id == user_id).first_or_404(description="Not Found")

    def get_by_username(self, name):
        """ Поиск пользователя по имени """
        return self.session.query(User).filter(User.username == name).first_or_404(description="Not Found")

    def check_id(self, user_id):
        """ Проверка занятости id """

        if self.session.query(User).get(user_id):
            raise TypeError("id занят")

    def get_commit(self):
        """ Commit через проверку соответствия полученных данных """

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise TypeError("Данные не соответствуют, либо уже существуют")

    def check_is_dict(self, data):
        """ Проверяем, являются ли данные словарём """

        if not isinstance(data, dict):
            raise TypeError("Неверный формат данных")

    def create(self, data):
        """ Создание данных нового пользователя """

        self.check_is_dict(data)
        self.check_id(data.get("id", 0))

        user = User(**data)
        self.session.add(user)
        self.get_commit()
        return user

    def update(self, user):
        """ Обновление данных пользователя """

        self.session.add(user)
        self.get_commit()
        return user

    def delete(self, user_id):
        """ Удаление данных пользователя """

        user = self.get_one(user_id)
        self.session.delete(user)
        self.session.commit()
