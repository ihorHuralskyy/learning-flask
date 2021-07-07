from flask import Blueprint, request

import werkzeug

from flask import jsonify, abort

from .book_schemas import BookSchema, AuthorFilterSchema, BookIdSchema, BookNestedSchema

from .author_schemas import AuthorIdSchema

from .book_db_utils import *

book_bp = Blueprint("book", __name__, url_prefix="/books")


@book_bp.route("/", methods=["GET"])
def get_all_books():
    if request.args.get("author_fullname", None):
        schema_author = AuthorFilterSchema().load(request.args)
        authors_books = get_all_books_by_author_db(schema_author["author_fullname"])
        return jsonify(BookSchema(many=True).dump(authors_books))

    books = get_all_books_db()
    return jsonify(BookSchema(many=True).dump(books))


@book_bp.route("/<book_id>", methods=["GET"])
def get_book_by_id(book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)

    book = get_book_by_id_db(book_id_schema["id"])

    return BookSchema().dump(book)


@book_bp.route("/", methods=["POST"])
def create_book():
    schema_book = BookNestedSchema().load(request.json)

    try:
        get_book_by_id_db(schema_book["id"])
        message = {"error": f"book with id:{schema_book['id']} already exists"}
        return message, 409
    except werkzeug.exceptions.NotFound:
        create_book_db(schema_book)
        return schema_book, 201


@book_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    schema_book_dict = {"id": book_id, **request.json}
    schema_book = BookNestedSchema().load(schema_book_dict)

    update_book_db(**schema_book)

    return schema_book, 200


@book_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)

    book = delete_book_db(book_id_schema["id"])

    return BookSchema().dump(book)


@book_bp.route("/<book_id>/authors/<author_id>", methods=["PUT"])
def add_author_for_book(book_id, author_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    add_relation_for_book_db(book_id_schema["id"], author_id_schema["id"])

    book = get_book_by_id_db(book_id_schema["id"])

    return BookSchema().dump(book), 200


@book_bp.route("/<book_id>/authors/<author_id>", methods=["DELETE"])
def remove_author_for_book(book_id, author_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    remove_relation_for_book_db(book_id_schema["id"], author_id_schema["id"])

    book = get_book_by_id_db(book_id_schema["id"])

    return BookSchema().dump(book)
