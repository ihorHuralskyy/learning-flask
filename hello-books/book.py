from flask import (
    Blueprint, request
)

from flask import jsonify, Response

bp = Blueprint('book', __name__)

books = [{"id": 1, "author": "Brown", "title": "Origin"}, {"id": 2, "author": "Rowling", "title": "Harry Potter"},
         {"id": 3, "author": "Shevchenko", "title": "Kobzar"}]


@bp.route("/")
def get_all_books():
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
    book_id = request.json.get("id", None)
    title = request.json.get("title", None)
    author = request.json.get("author", None)

    if not book_id or not title or not author:
        return Response(status=400)

    for book in books:
        if book["id"] == book_id:
            return Response(status=409)

    new_book = {
        "id": book_id,
        "author": author,
        "title": title,
    }
    books.append(new_book)

    return jsonify(new_book), 201


@bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        return Response(status=400)

    data = request.get_json()
    author = data.get("author", None)
    title = data.get("title", None)

    if not author or not title:
        return Response(status=400)

    for book in books:
        if book["id"] == book_id:
            book["author"] = author
            book["title"] = title
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
