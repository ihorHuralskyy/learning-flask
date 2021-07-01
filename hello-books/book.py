from flask import (
    Blueprint, request
)

from flask import jsonify, Response

bp = Blueprint('book', __name__)

books = [{"author": "Brown", "title": "Origin"}, {"author": "Rowling", "title": "Harry Potter"},
         {"author": "Shevchenko", "title": "Kobzar"}]


@bp.route("/")
def get_all_books():
    return jsonify(books)


@bp.route("/<book_title>")
def get_book_by_title(book_title):
    for book in books:
        if book["title"] == book_title:
            return jsonify(book)
    return Response(status=404)


@bp.route("/create", methods=["POST"])
def create_book():
    title = request.json.get("title", None)
    author = request.json.get("author", None)

    if not title or not author:
        return Response(status=400)

    for book in books:
        if book["title"] == title:
            return Response(status=409)

    new_book = {
        "author": author,
        "title": title,
    }
    books.append(new_book)

    return jsonify(new_book), 201


@bp.route("/create_query", methods=["POST"])
def create_book_query():
    title = request.args.get("title", None)
    author = request.args.get("author", None)

    if not title or not author:
        return Response(status=400)

    for book in books:
        if book["title"] == title:
            return Response(status=409)

    new_book = {
        "author": author,
        "title": title,
    }
    books.append(new_book)

    return jsonify(new_book), 201


@bp.route("/<book_title>/update", methods=["POST"])
def update_book(book_title):
    data = request.get_json()
    author = data.get("author", None)

    if not author:
        return Response(status=400)

    for book in books:
        if book["title"] == book_title:
            book["author"] = author
            return jsonify(book), 200

    return Response(status=404)


@bp.route("/<book_title>/delete", methods=["DELETE"])
def delete_book(book_title):

    for book in books:
        if book["title"] == book_title:
            books.remove(book)
            return jsonify(book), 200

    return Response(status=404)
