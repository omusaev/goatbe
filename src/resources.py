# -*- coding: utf-8 -*-

import json
import falcon

from decorators import db_transaction

from models import DBSession

__ALL__ = (
    'BaseResource',
    'Ping',
)


class BaseResource(object):

    url = None

    @property
    def url(self):
        return self.url

    def __init__(self):
        self.db_session = DBSession()

    @db_transaction
    def on_get(self, *args, **kwargs):
        if hasattr(self, 'get'):
            return self.get(*args, **kwargs)
        raise falcon.HTTPError(
            falcon.HTTP_405, None, "The request method is not allowed for this resource"
        )

    @db_transaction
    def on_post(self, *args, **kwargs):
        if hasattr(self, 'post'):
            return self.post(*args, **kwargs)
        raise falcon.HTTPError(
            falcon.HTTP_405, None, "The request method is not allowed for this resource"
        )


class Ping(BaseResource):

    url = '/ping/'

    def get(self, req, resp):
        resp.body = json.dumps('Pong')
