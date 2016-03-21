# -*- coding: utf-8 -*-

from voluptuous import (
    Required, All,
)

from common.exceptions import AuthenticationRequiredException
from common.resources.base import BaseResource

from events import EVENT_TYPES

__all__ = (
    'EventTypes',
)


class EventTypes(BaseResource):

    url = '/events/types/'

    data_schema = {
        Required('lang'): All(unicode),
    }

    def get(self):
        # TODO: create auth_required validator or decorator
        if not self.account_info:
            raise AuthenticationRequiredException

        lang = self.get_param('lang')
        response_data = {}

        # TODO: create admin panel
        for event_type, data in EVENT_TYPES.iteritems():
            response_data.update({
                event_type: {
                    'title': data.get(lang, {}).get('title'),
                    'description': data.get(lang, {}).get('description'),
                }
            })

        self.response_data = response_data
