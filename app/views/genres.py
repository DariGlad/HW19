from flask import request, jsonify
from flask_restx import Resource, Namespace

from app.dao.schema.genre import GenreSchema
from app.helpers.decorators import auth_required, admin_required
from app.implemented import genres_service

genre_ns = Namespace("genres")  # Создаём Namespace жанров
genre_schema = GenreSchema()  # Схема для сериализации одного жанра
genres_schema = GenreSchema(many=True)  # Схема для сериализации нескольких жанров


@genre_ns.route("/")
class GenresView(Resource):
    """ CBV жанров
        GET получение данных всех жанров
        POST добавление данных нового жанра
    """

    @auth_required
    def get(self):
        genres = genres_service.get_all()
        return genres_schema.dump(genres), 200

    @admin_required
    def post(self):
        json_req = request.json
        try:
            new_genre = genres_service.create(json_req)
        except TypeError as e:
            return str(e), 400
        res = jsonify(genre_schema.dump(new_genre))
        res.status_code = 201
        res.headers["location"] = new_genre.id  # Добавляем расположение созданного жанра в заголовок
        return res


@genre_ns.route("/<int:genre_id>/")
class GenreView(Resource):
    """ CBV жанра
        GET получение данных жанра по id
        PUT изменяем данные жанра по id
        PATCH частичное изменение данных жанра по id
        DELETE удаляем данные жанра по id
    """

    @auth_required
    def get(self, genre_id):
        genre = genres_service.get_one(genre_id)
        return genre_schema.dump(genre), 200

    @admin_required
    def put(self, genre_id):
        json_req = request.json
        try:
            genres_service.check_is_dict(json_req)
            genre = genres_service.update(genre_id, json_req)
        except TypeError as e:
            return str(e), 400

        return genre_schema.dump(genre), 201

    @admin_required
    def patch(self, genre_id):
        json_req = request.json
        try:
            genres_service.check_is_dict(json_req)
            genre = genres_service.update_partial(genre_id, json_req)
        except TypeError as e:
            return str(e), 400

        return genre_schema.dump(genre), 201

    @admin_required
    def delete(self, genre_id):
        genres_service.delete(genre_id)

        return "", 204
