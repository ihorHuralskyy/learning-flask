from hello_books import db
from sqlalchemy.sql import func


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())


class Book(BaseModel):
    __tablename__ = "book"
    title = db.Column(db.String(50))
    pages = db.Column(db.Integer)
    authors = db.relationship("Author", backref=db.backref("books", lazy="dynamic"))


class Author(BaseModel):
    __tablename__ = "author"
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    fullname = db.column_property(firstname + " " + lastname)


class BookAuthor(BaseModel):
    __tablename__ = "book_author"
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
