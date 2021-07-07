from marshmallow import Schema, fields, validate


class AuthorNestedSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    firstname = fields.String(required=True, validate=validate.Length(max=50))
    lastname = fields.String(required=True, validate=validate.Length(max=50))


class AuthorIdSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))


import hello_books.book_schemas as book_schemas


class AuthorSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    firstname = fields.String(required=True, validate=validate.Length(max=50))
    lastname = fields.String(required=True, validate=validate.Length(max=50))
    books = fields.Nested(book_schemas.BookNestedSchema, many=True)
