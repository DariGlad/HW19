from sqlalchemy.exc import IntegrityError

from app.dao.model.movie import Movie


class MoviesDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """ Возвращает данные всех фильмов """
        return self.session.query(Movie).all()

    def get_one(self, movie_id):
        """ Возвращает данные по id фильма, либо ошибку 404 """
        return self.session.query(Movie).filter(Movie.id == movie_id).first_or_404(description="Not Found")

    def check_id(self, movie_id):
        """ Проверка занятости id """
        if self.session.query(Movie).get(movie_id):
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
        """ Создание данных нового фильма """
        self.check_is_dict(data)
        self.check_id(data.get("id", None))

        movie = Movie(**data)
        self.session.add(movie)
        self.get_commit()
        return movie

    def update(self, movie):
        """ Обновление данных фильма """
        self.session.add(movie)
        self.get_commit()
        return movie

    def delete(self, movie_id):
        """ Удаление данных фильма """
        movie = self.get_one(movie_id)
        self.session.delete(movie)
        self.session.commit()

    def get_director_id(self, director_id):
        """ Поиск фильмов по id режиссёра """
        return self.session.query(Movie). \
            filter(Movie.director_id == director_id). \
            all()

    def get_genre_id(self, genre_id):
        """ Поиск фильмов по id жанра """
        return self.session.query(Movie). \
            filter(Movie.genre_id == genre_id). \
            all()

    def get_year(self, year):
        """ Поиск фильмов по году выпуска """
        return self.session.query(Movie). \
            filter(Movie.year == year). \
            all()
