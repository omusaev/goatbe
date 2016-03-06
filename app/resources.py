# -*- coding: utf-8 -*-

import json

from common.base import BaseResource

__all__ = (
    'Ping',
)


class Ping(BaseResource):

    url = '/ping/'

    def get(self, req, resp):
        resp.body = json.dumps('Pong')
