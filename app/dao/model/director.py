from app.setup_db import db


class Director(db.Model):
    """ Модель режиссёра """
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
