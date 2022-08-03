from sqlalchemy.exc import IntegrityError

from app.dao.model.director import Director


class DirectorsDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """ Возвращает данные всех режиссёров """

        return self.session.query(Director).all()

    def get_one(self, director_id):
        """ Возвращает данные по id режиссёра, либо ошибку 404 """

        return self.session.query(Director).filter(Director.id == director_id).first_or_404(description="Not Found")

    def check_id(self, director_id):
        """ Проверка занятости id """

        if self.session.query(Director).get(director_id):
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
        """ Создание данных нового режиссёра """

        self.check_is_dict(data)
        self.check_id(data.get("id", None))

        director = Director(**data)
        self.session.add(director)
        self.get_commit()
        return director

    def update(self, director):
        """ Обновление данных режиссёра """

        self.session.add(director)
        self.get_commit()
        return director

    def delete(self, director_id):
        """ Удаление данных режиссёра """

        director = self.get_one(director_id)
        self.session.delete(director)
        self.session.commit()
