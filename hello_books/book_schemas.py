from marshmallow import Schema, fields, validate


class BookNestedSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    title = fields.String(required=True, validate=validate.Length(max=50))
    pages = fields.Integer(required=True, validate=validate.Range(min=1))


import hello_books.author_schemas as author_schemas


class AuthorFilterSchema(Schema):
    author_fullname = fields.String(required=True, validate=validate.Length(max=101))


class BookIdSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))


class BookSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    title = fields.String(required=True, validate=validate.Length(max=50))
    pages = fields.Integer(required=True, validate=validate.Range(min=1))
    authors = fields.Nested(author_schemas.AuthorNestedSchema, many=True, required=True)
