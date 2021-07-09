from sqlalchemy.exc import SQLAlchemyError

from hello_books import db


def commit_rollback_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(e)

    return wrapper
