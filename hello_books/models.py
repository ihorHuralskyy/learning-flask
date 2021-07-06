from hello_books import db

book_author = db.Table(
    "book_author",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    pages = db.Column(db.Integer)
    authors = db.relationship(
        "Author", secondary=book_author, backref=db.backref("books", lazy="dynamic")
    )


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(70))
