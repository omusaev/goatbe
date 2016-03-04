# -*- coding: utf-8 -*-

import json
import falcon

from utils.decorators import db_transaction

from common.base import BaseResource

from models import DBSession

__ALL__ = (
    'Ping',
)


class Ping(BaseResource):

    url = '/ping/'

    def get(self, req, resp):
        resp.body = json.dumps('Pong')
