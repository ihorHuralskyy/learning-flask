from marshmallow import Schema, fields, validate


class BookNestedSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    title = fields.String(required=True, validate=validate.Length(max=50))
    pages = fields.Integer(required=True, validate=validate.Range(min=1))


class AuthorFilterSchema(Schema):
    author_fullname = fields.String(required=True, validate=validate.Length(max=101))


class BookIdSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))


class AuthorNestedSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    firstname = fields.String(required=True, validate=validate.Length(max=50))
    lastname = fields.String(required=True, validate=validate.Length(max=50))


class AuthorIdSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))


class AuthorSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    firstname = fields.String(required=True, validate=validate.Length(max=50))
    lastname = fields.String(required=True, validate=validate.Length(max=50))
    books = fields.Nested(BookNestedSchema, many=True)


class BookSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    title = fields.String(required=True, validate=validate.Length(max=50))
    pages = fields.Integer(required=True, validate=validate.Range(min=1))
    authors = fields.Nested(AuthorNestedSchema, many=True, required=True)


class BookInputSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(max=50))
    pages = fields.Integer(required=True, validate=validate.Range(min=1))


class AuthorInputSchema(Schema):
    firstname = fields.String(required=True, validate=validate.Length(max=50))
    lastname = fields.String(required=True, validate=validate.Length(max=50))
