from sqlalchemy.exc import IntegrityError

from app.dao.model.genre import Genre


class GenresDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """ Возвращает данные всех жанров """

        return self.session.query(Genre).all()

    def get_one(self, genre_id):
        """ Возвращает данные по id жанра, либо ошибку 404 """

        return self.session.query(Genre).filter(Genre.id == genre_id).first_or_404(description="Not Found")

    def check_id(self, genre_id):
        """ Проверка занятости id """

        if self.session.query(Genre).get(genre_id):
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
        """ Создание данных нового жанра """

        self.check_is_dict(data)
        self.check_id(data.get("id", None))

        genre = Genre(**data)
        self.session.add(genre)
        self.get_commit()
        return genre

    def update(self, genre):
        """ Обновление данных жанра """

        self.session.add(genre)
        self.get_commit()
        return genre

    def delete(self, genre_id):
        """ Удаление данных жанра """

        genre = self.get_one(genre_id)
        self.session.delete(genre)
        self.session.commit()
