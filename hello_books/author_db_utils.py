from .models import Book, Author
from hello_books import db


def get_all_authors_db():
    return Author.query.all()


def get_author_by_id_db(id):
    return Author.query.filter_by(id=id).first_or_404(
        description=f"no author with id:{id}"
    )


from .book_db_utils import get_book_by_id_db


def create_author_db(author):
    new_author = Author(**author)
    db.session.add(new_author)
    db.session.commit()


def update_author_db(id, **updated_author):
    author = get_author_by_id_db(id)
    for key, value in updated_author.items():
        setattr(author, key, value)
    db.session.commit()


def delete_author_db(id):
    author = get_author_by_id_db(id)
    db.session.delete(author)
    db.session.commit()


def add_relation_for_author_db(id, book_id):
    author = get_author_by_id_db(id)
    book = get_book_by_id_db(book_id)
    if book not in author.books:
        author.books.append(book)
        db.session.commit()


def remove_relation_for_author_db(id, book_id):
    author = get_author_by_id_db(id)
    book = get_book_by_id_db(book_id)
    if book in author.books:
        author.books.remove(book)
        db.session.commit()
