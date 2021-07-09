from flask import Blueprint, request

import werkzeug

from flask import jsonify, abort

from .schemas import (
    BookSchema,
    AuthorFilterSchema,
    BookIdSchema,
    BookNestedSchema,
    AuthorIdSchema,
    BookInputSchema,
)

from . import book_db_utils as book_db

from . import author_db_utils as author_db

book_bp = Blueprint("book", __name__, url_prefix="/books")


@book_bp.route("/", methods=["GET"])
def get_all_books():
    if request.args.get("author_fullname", None):
        schema_author = AuthorFilterSchema().load(request.args)
        authors_books = book_db.get_all_books_by_author(
            schema_author["author_fullname"]
        )
        return jsonify(BookSchema(many=True).dump(authors_books))

    books = book_db.get_all_books()
    return jsonify(BookSchema(many=True).dump(books))


@book_bp.route("/<book_id>", methods=["GET"])
def get_book_by_id(book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)

    book = book_db.get_book_by_id(book_id_schema["id"])

    return BookSchema().dump(book)


@book_bp.route("/", methods=["POST"])
def create_book():
    schema_book = BookInputSchema().load(request.json)
    created_book = book_db.create_book(schema_book)
    output_book = BookSchema().dump(created_book)
    return output_book, 201


@book_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    schema_book_dict = {"id": book_id, **request.json}
    schema_book = BookNestedSchema().load(schema_book_dict)

    book_db.update_book(**schema_book)

    return schema_book, 200


@book_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)

    book = book_db.delete_book(book_id_schema["id"])

    return BookSchema().dump(book)


@book_bp.route("/<book_id>/authors/<author_id>", methods=["PUT"])
def add_author_for_book(book_id, author_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)
    author = author_db.get_author_by_id(author_id_schema["id"])

    book_db.add_relation_for_book(book_id_schema["id"], author)

    book = book_db.get_book_by_id(book_id_schema["id"])

    return BookSchema().dump(book), 200


@book_bp.route("/<book_id>/authors/<author_id>", methods=["DELETE"])
def remove_author_for_book(book_id, author_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)
    author = author_db.get_author_by_id(author_id_schema["id"])

    book_db.remove_relation_for_book(book_id_schema["id"], author)

    book = book_db.get_book_by_id(book_id_schema["id"])

    return BookSchema().dump(book)
