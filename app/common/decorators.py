# -*- coding: utf-8 -*-

import copy
import json

import falcon

from functools import wraps

from voluptuous import Schema, Invalid

from settings import DBSession


__ALL__ = (
    'db_transaction',
    'data_required',
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


def data_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        req = args[1]
        resp = args[2]
        request_data = copy.deepcopy(json.load(req.stream))

        validator = Schema(args[0].data_schema)

        try:
            validator(request_data)
        except Invalid as e:
            resp.status = falcon.HTTP_409
            resp.body = json.dumps(
                {
                    'error': str(e),
                    'data': request_data
                }
            )
            return

        kwargs.update({'data': request_data})

        return func(*args, **kwargs)

    return wrapper