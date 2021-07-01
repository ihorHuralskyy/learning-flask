from flask import (
    Blueprint, request
)

from flask import jsonify, Response

from marshmallow import Schema, fields, ValidationError, validate

bp = Blueprint('book', __name__)

books = [{"id": 1, "author": "Brown", "title": "Origin"}, {"id": 2, "author": "Rowling", "title": "Harry Potter"},
         {"id": 3, "author": "Shevchenko", "title": "Kobzar"}]


class BookSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    author = fields.String(required=True, validate=validate.Length(max=50))
    title = fields.String(required=True, validate=validate.Length(max=30))


@bp.route("/")
def get_all_books():
    author = request.args.get("author", None)
    if author:
        authors_books = [book for book in books if book["author"] == author]
        return jsonify(authors_books)

    return jsonify(books)


@bp.route("/<book_id>")
def get_book_by_id(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        return Response(status=400)

    for book in books:
        if book["id"] == book_id:
            return jsonify(book)
    return Response(status=404)


@bp.route("/create", methods=["POST"])
def create_book():
    try:
        schema_book = BookSchema().load(request.json)
    except ValidationError as error:
        return jsonify(error), 400

    for book in books:
        if book["id"] == schema_book["id"]:
            return Response(status=409)

    books.append(schema_book)

    return jsonify(schema_book), 201


@bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    try:
        schema_book = BookSchema().load({**request.json, "id": book_id})
    except ValidationError as error:
        return jsonify(error), 400

    for book in books:
        if book["id"] == schema_book["id"]:
            book["author"] = schema_book["author"]
            book["title"] = schema_book["title"]
            return jsonify(book), 200

    return Response(status=404)


@bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        return Response(status=400)

    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return jsonify(book), 200

    return Response(status=404)
