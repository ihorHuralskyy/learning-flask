from flask import Blueprint, request

import werkzeug

from flask import jsonify

from .book_schemas import BookIdSchema

from .author_schemas import AuthorIdSchema, AuthorNestedSchema, AuthorSchema

from .author_db_utils import *

author_bp = Blueprint("author", __name__, url_prefix="/authors")


@author_bp.route("/", methods=["GET"])
def get_all_authors():
    authors = get_all_authors_db()
    return jsonify(AuthorSchema(many=True).dump(authors))


@author_bp.route("/<author_id>", methods=["GET"])
def get_author_by_id(author_id):
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    author = get_author_by_id_db(author_id_schema["id"])

    return AuthorSchema().dump(author)


@author_bp.route("/", methods=["POST"])
def create_author():
    schema_author = AuthorNestedSchema().load(request.json)

    try:
        get_author_by_id_db(schema_author["id"])
        message = {"error": f"author with id:{schema_author['id']} already exists"}
        return message, 409
    except werkzeug.exceptions.NotFound:
        create_author_db(schema_author)
        return schema_author, 201


@author_bp.route("/<author_id>", methods=["PUT"])
def update_author(author_id):
    schema_author_dict = {"id": author_id, **request.json}
    schema_author = AuthorNestedSchema().load(schema_author_dict)

    update_author_db(**schema_author)

    return schema_author, 200


@author_bp.route("/<author_id>", methods=["DELETE"])
def delete_author(author_id):
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    author = delete_author_db(author_id_schema["id"])

    return AuthorSchema().dump(author)


@author_bp.route("/<author_id>/books/<book_id>", methods=["PUT"])
def add_book_for_author(author_id, book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    add_relation_for_author_db(author_id_schema["id"], book_id_schema["id"])

    author = get_author_by_id_db(author_id_dict["id"])

    return AuthorSchema().dump(author), 200


@author_bp.route("/<author_id>/books/<book_id>", methods=["DELETE"])
def remove_book_for_author(author_id, book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)
    author_id_dict = {"id": author_id}
    author_id_schema = AuthorIdSchema().load(author_id_dict)

    remove_relation_for_author_db(author_id_schema["id"], book_id_schema["id"])

    author = get_author_by_id_db(author_id_dict["id"])

    return AuthorSchema().dump(author)
