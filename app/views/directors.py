from flask import request, jsonify
from flask_restx import Resource, Namespace

from app.dao.schema.director import DirectorSchema
from app.helpers.decorators import auth_required, admin_required
from app.implemented import directors_service

director_ns = Namespace("directors")  # Создаём Namespace режиссёров
director_schema = DirectorSchema()  # Схема для сериализации одного режиссёра
directors_schema = DirectorSchema(many=True)  # Схема для сериализации нескольких режиссёров


@director_ns.route("/")
class DirectorsView(Resource):
    """ CBV режисcёров
        GET получение данных всех режиссёров
        POST добавление данных нового режиссёра
    """

    @auth_required
    def get(self):
        directors = directors_service.get_all()
        return directors_schema.dump(directors), 200

    @admin_required
    def post(self):
        json_req = request.json
        try:
            new_director = directors_service.create(json_req)
        except TypeError as e:
            return str(e), 400
        res = jsonify(director_schema.dump(new_director))
        res.status_code = 201
        res.headers["location"] = new_director.id  # Добавляем расположение созданного режиссёра в заголовок
        return res


@director_ns.route("/<int:director_id>/")
class DirectorView(Resource):
    """ CBV режисcёра
        GET получение данных режиссёра по id
        PUT изменяем данные режиссёра по id
        PATCH частичное изменение данных режиссёра по id
        DELETE удаляем данные режиссёра по id
    """

    @auth_required
    def get(self, director_id):
        director = directors_service.get_one(director_id)
        return director_schema.dump(director), 200

    @admin_required
    def put(self, director_id):
        json_req = request.json
        try:
            directors_service.check_is_dict(json_req)
            director = directors_service.update(director_id, json_req)
        except TypeError as e:
            return str(e), 400

        return director_schema.dump(director), 201

    @admin_required
    def patch(self, director_id):
        json_req = request.json
        try:
            directors_service.check_is_dict(json_req)
            director = directors_service.update_partial(director_id, json_req)
        except TypeError as e:
            return str(e), 400

        return director_schema.dump(director), 201

    @admin_required
    def delete(self, director_id):
        directors_service.delete(director_id)

        return "", 204
