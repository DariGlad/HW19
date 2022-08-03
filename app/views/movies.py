from flask import request, jsonify
from flask_restx import Resource, Namespace, abort

from app.dao.schema.movie import MovieSchema
from app.helpers.decorators import auth_required, admin_required
from app.implemented import movies_service

movie_ns = Namespace("movies")  # Создаём Namespace фильмов
movie_schema = MovieSchema()  # Схема для сериализации одного фильма
movies_schema = MovieSchema(many=True)  # Схема для сериализации нескольких фильмов


@movie_ns.route("/")
class MoviesView(Resource):
    """ CBV фильмов
        GET получение данных всех фильмов,
        по id режиссёра или жанра,
        по году выпуска
        POST добавление данных нового фильма
    """

    @auth_required
    @movie_ns.doc(description="При заполнении id режиссёра, выведутся фильмы данного режиссёра\n"
                              "При заполнении id жанра, выведутся фильмы данного жанра\n"
                              "При заполнении года выпуска выведутся фильмы\n"
                              "При незаполненных полях, выведутся все данные",
                  params={
                      "director_id": "id режиссёра",
                      "genre_id": "id жанра",
                      "year": "год выпуска"
                  })
    def get(self):
        req_args = request.args
        if len(req_args) > 1:  # Если параметров больше одного выдаст сообщение об этом
            return "Заполните только одно поле"
        if req_args:
            movies = movies_service.get_find(req_args)  # Поиск по параметрам
        else:
            movies = movies_service.get_all()
        if not movies:
            raise abort(404)
        return movies_schema.dump(movies), 200

    @admin_required
    def post(self):
        json_req = request.json
        try:
            new_movie = movies_service.create(json_req)
        except TypeError as e:
            return str(e), 400
        res = jsonify(movie_schema.dump(new_movie))
        res.status_code = 201
        res.headers["location"] = new_movie.id  # Добавляем расположение созданного фильма в заголовок
        return res


@movie_ns.route("/<int:movie_id>/")
class MovieView(Resource):
    """ CBV фильма
        GET получение данных фильма по id
        PUT изменяем данные фильма по id
        PATCH частичное изменение данных фильма по id
        DELETE удаляем данные фильма по id
    """

    @auth_required
    def get(self, movie_id):
        movie = movies_service.get_one(movie_id)
        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, movie_id):
        json_req = request.json
        try:
            movies_service.check_is_dict(json_req)
            movie = movies_service.update(movie_id, json_req)
        except TypeError as e:
            return str(e), 400

        return movie_schema.dump(movie), 201

    @admin_required
    def patch(self, movie_id):
        json_req = request.json
        try:
            movies_service.check_is_dict(json_req)
            movie = movies_service.update_partial(movie_id, json_req)
        except TypeError as e:
            return str(e), 400

        return movie_schema.dump(movie), 201

    @admin_required
    def delete(self, movie_id):
        movies_service.delete(movie_id)

        return "", 204
