from flask import Flask
from flask_restx import Api
from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.dao.model.movie import Movie
from app.setup_db import db
from app.views.auth import auth_ns
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.movies import movie_ns
from app.views.users import user_ns
from data.data import data


def create_app(config_object):
    """функция создания основного объекта app """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    app.app_context().push()
    return app


def register_extensions(app):
    """функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)"""
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    # create_data(app, db)  # Раскомментировать для создания исходной базы данных


def create_data(app, db):
    """ Функция создания базы данных """
    with app.app_context():
        db.drop_all()
        db.create_all()

        directors = [Director(
            id=director["pk"],
            name=director["name"]
        ) for director in data["directors"]]

        genres = [Genre(
            id=genre["pk"],
            name=genre["name"]
        ) for genre in data["genres"]]

        movies = [Movie(
            id=movie["pk"],
            title=movie["title"],
            description=movie["description"],
            trailer=movie["trailer"],
            year=movie["year"],
            rating=movie["rating"],
            genre_id=movie["genre_id"],
            director_id=movie["director_id"]
        ) for movie in data["movies"]]

        with db.session.begin():
            db.session.add_all(directors)
            db.session.add_all(genres)
            db.session.add_all(movies)
