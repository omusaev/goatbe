# -*- coding: utf-8 -*-

from core.resources.base import BaseResource

from settings import CLIENT_SETTINGS

__all__ = (
    'ClientSettings',
)


class ClientSettings(BaseResource):

    url = '/v1/settings/'

    def post(self):
        self.response_data = CLIENT_SETTINGS
