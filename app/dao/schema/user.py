from marshmallow import Schema, fields


class UserSchema(Schema):
    """ Схема для сериализации пользователей """
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()