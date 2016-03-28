# -*- coding: utf-8 -*-

from common.resources.base import BaseResource
from voluptuous import (
    Optional, All, Range, Coerce,
)

__all__ = (
    'Ping',
)


class Ping(BaseResource):

    url = '/v1/ping/'

    data_schema = {
        Optional('number'): All(Coerce(int), Range(min=1, max=10)),
    }

    def get(self):
        if not self.session:
            from common.sessions.models import SessionManager
            self.session = SessionManager.create_session()

        self.session['counter'] = 1 if 'counter' not in self.session else self.session['counter'] + 1
        self.response_data = {
            'Answer': 'Pong',
            'Request counter': self.session['counter'],
        }
