# -*- coding: utf-8 -*-

from functools import wraps

from models import DBSession

__ALL__ = (
    'db_transaction',
    'expected_params',
)


def db_transaction(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
            DBSession.commit()
        except:
            DBSession.rollback()
            raise
        finally:
            DBSession.remove()

        return result

    return wrapper
