from flask import Blueprint, request

from flask import jsonify, abort

from .book_schemas import BookSchema, AuthorFilterSchema, BookIdSchema

bp = Blueprint("book", __name__, url_prefix="/books")

books = [
    {"id": 1, "author": "Brown", "title": "Origin"},
    {"id": 2, "author": "Rowling", "title": "Harry Potter"},
    {"id": 3, "author": "Shevchenko", "title": "Kobzar"},
    {"id": 4, "author": "Brown", "title": "Inferno"},
]


@bp.route("/", methods=["GET"])
def get_all_books():
    if request.args.get("author", None):
        schema_author = AuthorFilterSchema().load(request.args)
        authors_books = [
            book for book in books if book["author"] == schema_author["author"]
        ]
        return jsonify(BookSchema(many=True).dump(authors_books))

    return jsonify(BookSchema(many=True).dump(books))


@bp.route("/<book_id>", methods=["GET"])
def get_book_by_id(book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)

    for book in books:
        if book["id"] == book_id_schema["id"]:
            return BookSchema().load(book)

    abort(404, description=f"no book with id:{book_id_schema['id']}")


@bp.route("/", methods=["POST"])
def create_book():
    schema_book = BookSchema().load(request.json)

    for book in books:
        if book["id"] == schema_book["id"]:
            message = {"error": f"book with id:{schema_book['id']} already exists"}
            return message, 409

    books.append(schema_book)

    return schema_book, 201


@bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    schema_book_dict = {"id": book_id, **request.json}
    schema_book = BookSchema().load(schema_book_dict)

    for book in books:
        if book["id"] == schema_book["id"]:
            book["author"] = schema_book["author"]
            book["title"] = schema_book["title"]
            return schema_book, 200

    abort(404, description=f"no book with id:{schema_book['id']}")


@bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book_id_dict = {"id": book_id}
    book_id_schema = BookIdSchema().load(book_id_dict)

    for book in books:
        if book["id"] == book_id_schema["id"]:
            books.remove(book)
            return BookSchema().load(book)

    abort(404, description=f"no book with id:{book_id_schema['id']}")
