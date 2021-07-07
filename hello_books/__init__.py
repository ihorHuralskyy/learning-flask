from flask import Flask
from .error_handlers import validation_error, general_exception, entity_404
from marshmallow import ValidationError
from settings import SQLALCHEMY_DATABASE_URI
from flask_sqlalchemy import SQLAlchemy

# from functools import partial

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .book import book_bp

    app.register_blueprint(book_bp)

    from .author import author_bp

    app.register_blueprint(author_bp)
    # app.register_error_handler(
    #     ValidationError, partial(error_handler, status_code=codes.bad_request)
    # )

    app.register_error_handler(ValidationError, validation_error)
    app.register_error_handler(Exception, general_exception)
    app.register_error_handler(404, entity_404)

    with app.app_context():
        from .models import Author, Book, BookAuthor

        db.create_all()

    return app
