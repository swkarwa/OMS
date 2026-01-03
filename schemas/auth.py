from marshmallow import Schema, fields


class Login(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
