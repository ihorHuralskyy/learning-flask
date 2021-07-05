from flask import Flask
from .book_error_handlers import book_validation_error, book_general_exception, book_404
from marshmallow import ValidationError

# from functools import partial


def create_app():
    app = Flask(__name__)

    from .book import bp

    app.register_blueprint(bp)

    # app.register_error_handler(
    #     ValidationError, partial(error_handler, status_code=codes.bad_request)
    # )

    app.register_error_handler(ValidationError, book_validation_error)
    app.register_error_handler(Exception, book_general_exception)
    app.register_error_handler(404, book_404)

    return app
