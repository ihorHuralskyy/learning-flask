from sqlalchemy import UniqueConstraint

from hello_books import db
from sqlalchemy.sql import func


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())


class Book(BaseModel):
    __tablename__ = "books"
    title = db.Column(db.String(50))
    pages = db.Column(db.Integer)
    authors = db.relationship(
        "Author",
        secondary="books_authors",
        backref=db.backref("books", lazy="dynamic"),
        uselist=True,
    )
    __table_args__ = (db.UniqueConstraint("title", "pages"),)


class Author(BaseModel):
    __tablename__ = "authors"
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    fullname = db.column_property(firstname + " " + lastname)
    __table_args__ = (db.UniqueConstraint("firstname", "lastname"),)


class BookAuthor(BaseModel):
    __tablename__ = "books_authors"
    books_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    authors_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
