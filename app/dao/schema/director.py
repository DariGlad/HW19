from marshmallow import Schema, fields


class DirectorSchema(Schema):
    """ Схема для сериализации режиссёра """
    id = fields.Int(dump_only=True)
    name = fields.Str()
