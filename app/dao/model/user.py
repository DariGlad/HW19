from app.setup_db import db


class User(db.Model):
    """ Модель пользователя """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(50))
