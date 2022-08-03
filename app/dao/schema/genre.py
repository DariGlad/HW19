from marshmallow import Schema, fields


class GenreSchema(Schema):
    """ Схема для сериализации жанра """
    id = fields.Int(dump_only=True)
    name = fields.Str()
