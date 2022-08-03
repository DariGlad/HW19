class MoviesService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        """ Возвращает данные всех фильмов """
        return self.dao.get_all()

    def get_one(self, movie_id):
        """ Возвращает данные по id фильма """
        return self.dao.get_one(movie_id)

    def check_is_dict(self, data):
        """ Проверяем, являются ли данные словарём """
        return self.dao.check_is_dict(data)

    def create(self, data):
        """ Создание данных нового фильма """
        return self.dao.create(data)

    def update(self, movie_id, data):
        """ Обновление данных фильма по id """
        movie = self.get_one(movie_id)
        movie.id = data.get("id")
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")
        return self.dao.update(movie)

    def update_partial(self, movie_id, data):
        """ Частичное обновление данных фильма по id """

        movie = self.get_one(movie_id)
        if "id" in data:
            movie.id = data.get("id")
        if "title" in data:
            movie.title = data.get("title")
        if "description" in data:
            movie.description = data.get("description")
        if "trailer" in data:
            movie.trailer = data.get("trailer")
        if "year" in data:
            movie.year = data.get("year")
        if "rating" in data:
            movie.rating = data.get("rating")
        if "genre_id" in data:
            movie.genre_id = data.get("genre_id")
        if "director_id" in data:
            movie.director_id = data.get("director_id")
        return self.dao.update(movie)

    def delete(self, movie_id):
        """ Удаление данных фильма по id """
        self.dao.delete(movie_id)

    def get_find(self, data):
        """ Поиск по полученным параметрам """
        if not data:
            return None
        if data.get("director_id"):
            return self.dao.get_director_id(data.get("director_id", type=int))
        if data.get("genre_id"):
            return self.dao.get_genre_id(data.get("genre_id", type=int))
        if data.get("year"):
            return self.dao.get_year(data.get("year", type=int))
