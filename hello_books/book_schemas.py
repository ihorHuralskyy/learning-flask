from marshmallow import Schema, fields, validate


class BookSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    author = fields.String(required=True, validate=validate.Length(max=50))
    title = fields.String(required=True, validate=validate.Length(max=30))


class AuthorFilterSchema(Schema):
    author = fields.String(required=True, validate=validate.Length(max=50))


class BookIdSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
