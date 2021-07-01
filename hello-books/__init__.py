from flask import Flask


def create_app():
    app = Flask(__name__)

    from . import book

    app.register_blueprint(book.bp)

    return app
