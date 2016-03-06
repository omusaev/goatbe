# -*- coding: utf-8 -*-

import copy
import json

import falcon

from functools import wraps

from voluptuous import Schema, Invalid

from settings import DBSession

__all__ = (
    'db_transaction',
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
