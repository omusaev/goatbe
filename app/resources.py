# -*- coding: utf-8 -*-

from voluptuous import (
    Optional, All, Range, Coerce,
)

from common.base import BaseResource

__all__ = (
    'Ping',
)


class Ping(BaseResource):

    url = '/ping/'

    data_schema = {
        Optional('number'): All(Coerce(int), Range(min=1, max=10)),
    }

    def get(self):
        self.response_data = 'Pong'
