from flask import Blueprint, request

import werkzeug

from flask import jsonify

from .schemas import (
    AuthorIdSchema,
    AuthorNestedSchema,
    AuthorSchema,
    BookIdSchema,
    AuthorInputSchema,
)

from . import author_db_utils as author_db

from . import book_db_utils as book_db


author_bp = Blueprint("author", __name__, url_prefix="/authors")


@author_bp.route("/", methods=["GET"])
def get_all_authors():
    authors = author_db.get_all_authors()
    return jsonify(AuthorSchema(many=True).dump(authors))


@author_bp.route("/<author_id>", methods=["GET"])
def get_author_by_id(author_id):
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    author = author_db.get_author_by_id(author_id_schema["id"])

    return AuthorSchema().dump(author)


@author_bp.route("/", methods=["POST"])
def create_author():
    schema_author = AuthorInputSchema().load(request.json)
    created_author = author_db.create_author(schema_author)
    output_author = AuthorSchema().dump(created_author)
    return output_author, 201


@author_bp.route("/<author_id>", methods=["PUT"])
def update_author(author_id):
    schema_author_dict = {"id": author_id, **request.json}
    schema_author = AuthorNestedSchema().load(schema_author_dict)

    author_db.update_author(**schema_author)

    return schema_author, 200


@author_bp.route("/<author_id>", methods=["DELETE"])
def delete_author(author_id):
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    author = author_db.delete_author(author_id_schema["id"])

    return AuthorSchema().dump(author)


@author_bp.route("/<author_id>/books/<book_id>", methods=["PUT"])
def add_book_for_author(author_id, book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)
    book = book_db.get_book_by_id(book_id_schema["id"])

    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    author_db.add_relation_for_author(author_id_schema["id"], book)

    author = author_db.get_author_by_id(author_id_dict["id"])

    return AuthorSchema().dump(author), 200


@author_bp.route("/<author_id>/books/<book_id>", methods=["DELETE"])
def remove_book_for_author(author_id, book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)
    book = book_db.get_book_by_id(book_id_schema["id"])

    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    author_db.remove_relation_for_author(author_id_schema["id"], book)

    author = author_db.get_author_by_id(author_id_dict["id"])

    return AuthorSchema().dump(author)
