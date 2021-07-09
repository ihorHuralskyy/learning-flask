from .models import Book, Author
from hello_books import db


def get_all_books():
    return Book.query.all()


def get_all_books_by_author(fullname):
    return Book.query.filter(Book.authors.any(fullname=fullname))


def get_book_by_id(id):
    return Book.query.filter_by(id=id).first_or_404(description=f"no book with id:{id}")


def create_book(book):
    new_book = Book(**book)
    db.session.add(new_book)
    db.session.commit()
    return new_book


def update_book(id, **updated_book):
    book = get_book_by_id(id)
    for key, value in updated_book.items():
        setattr(book, key, value)
    db.session.commit()


def delete_book(id):
    book = get_book_by_id(id)
    db.session.delete(book)
    db.session.commit()
    return book


def add_relation_for_book(id, author):
    book = get_book_by_id(id)
    if author not in book.authors:
        book.authors.append(author)
        db.session.commit()


def remove_relation_for_book(id, author):
    book = get_book_by_id(id)
    if author in book.authors:
        book.authors.remove(author)
        db.session.commit()
