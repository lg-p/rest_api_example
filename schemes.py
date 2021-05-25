from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=250)])
    message = fields.String(dump_only=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    login = fields.String(required=True, validate=[validate.Length(max=250)])
    password = fields.String(required=True, validate=[validate.Length(max=120)])
    items = fields.Nested(ItemSchema, many=True, dump_only=True)
    message = fields.String(dump_only=True)


class AuthenticationSchema(Schema):
    access_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)


class SendItemSchema(Schema):
    id = fields.Integer()
    login = fields.String(required=True, validate=[validate.Length(max=250)])


class URLSchema(Schema):
    link = fields.String(required=True)
