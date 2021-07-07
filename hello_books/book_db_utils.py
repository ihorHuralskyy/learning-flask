from .models import Book, Author
from hello_books import db


def get_all_books_db():
    return Book.query.all()


def get_all_books_by_author_db(fullname):
    return Book.query.filter(Book.authors.any(fullname=fullname))


def get_book_by_id_db(id):
    return Book.query.filter_by(id=id).first_or_404(description=f"no book with id:{id}")


from .author_db_utils import get_author_by_id_db


def create_book_db(book):
    new_book = Book(**book)
    db.session.add(new_book)
    db.session.commit()
    return new_book


def update_book_db(id, **updated_book):
    book = get_book_by_id_db(id)
    for key, value in updated_book.items():
        setattr(book, key, value)
    db.session.commit()


def delete_book_db(id):
    book = get_book_by_id_db(id)
    db.session.delete(book)
    db.session.commit()
    return book


def add_relation_for_book_db(id, author_id):
    book = get_book_by_id_db(id)
    author = get_author_by_id_db(author_id)
    if author not in book.authors:
        book.authors.append(author)
        db.session.commit()


def remove_relation_for_book_db(id, author_id):
    book = get_book_by_id_db(id)
    author = get_author_by_id_db(author_id)
    if author in book.authors:
        book.authors.remove(author)
        db.session.commit()
