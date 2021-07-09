from .models import Book, Author
from hello_books import db
from .utils import commit_rollback_decorator


def get_all_authors():
    return Author.query.all()


def get_author_by_id(id):
    return Author.query.filter_by(id=id).first_or_404(
        description=f"no author with id:{id}"
    )


@commit_rollback_decorator
def create_author(author):
    new_author = Author(**author)
    db.session.add(new_author)
    return new_author


def update_author(id, **updated_author):
    author = get_author_by_id(id)
    for key, value in updated_author.items():
        setattr(author, key, value)
    db.session.commit()


def delete_author(id):
    author = get_author_by_id(id)
    db.session.delete(author)
    db.session.commit()


def add_relation_for_author(id, book):
    author = get_author_by_id(id)
    if book not in author.books:
        author.books.append(book)
        db.session.commit()


def remove_relation_for_author(id, book):
    author = get_author_by_id(id)
    if book in author.books:
        author.books.remove(book)
        db.session.commit()
