from flask import request
from flask_restx import Namespace, Resource

from app.implemented import auth_service

auth_ns = Namespace("auth")


@auth_ns.route("/")
class AuthView(Resource):
    """ CBV аутентификации
     POST - получение токенов пользователя
     PUT - обновление токенов пользователя """

    def post(self):
        json_req = request.json

        username = json_req.get("username", None)
        password = json_req.get("password", None)

        if None in [username, password]:
            return "", 400

        return auth_service.generate_tokens(username, password)

    def put(self):
        json_req = request.json

        token = json_req.get("refresh_token")
        return auth_service.approve_refresh_token(token)
