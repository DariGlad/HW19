from flask import request, jsonify
from flask_restx import Resource, Namespace

from app.dao.schema.user import UserSchema
from app.implemented import users_service

user_ns = Namespace("users")  # Создаём Namespace пользователей
user_schema = UserSchema()  # Схема для сериализации одного пользователя
users_schema = UserSchema(many=True)  # Схема для сериализации нескольких пользователей


@user_ns.route("/")
class UsersView(Resource):
    """ CBV пользователей
        GET получение данных всех пользователей
        POST добавление данных нового пользователя
    """

    def get(self):
        users = users_service.get_all()
        return users_schema.dump(users), 200

    def post(self):
        json_req = request.json
        try:
            new_user = users_service.create(json_req)
        except TypeError as e:
            return str(e), 400
        res = jsonify(user_schema.dump(new_user))
        res.status_code = 201
        res.headers["location"] = new_user.id  # Добавляем расположение созданного пользователя в заголовок
        return res


@user_ns.route("/<int:user_id>/")
class UserView(Resource):
    """ CBV пользователя
        GET получение данных пользователя по id
        PUT изменяем данные пользователя по id
        PATCH частичное изменение данных пользователя по id
        DELETE удаляем данные пользователя по id
    """

    def get(self, user_id):
        user = users_service.get_one(user_id)
        return user_schema.dump(user), 200

    def put(self, user_id):
        json_req = request.json
        try:
            users_service.check_is_dict(json_req)
            user = users_service.update(user_id, json_req)
        except TypeError as e:
            return str(e), 400

        return user_schema.dump(user), 201

    def patch(self, user_id):
        json_req = request.json
        try:
            users_service.check_is_dict(json_req)
            user = users_service.update_partial(user_id, json_req)
        except TypeError as e:
            return str(e), 400

        return user_schema.dump(user), 201

    def delete(self, user_id):
        users_service.delete(user_id)

        return "", 204
