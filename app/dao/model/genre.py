from app.setup_db import db


class Genre(db.Model):
    """ Модель жанра """
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
