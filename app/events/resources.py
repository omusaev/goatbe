# -*- coding: utf-8 -*-

from voluptuous import (
    Required, All,
)

from accounts.validators import AuthRequiredValidator

from common.resources.base import BaseResource

from events import EVENT_TYPES

__all__ = (
    'EventsTypes',
)


class EventsTypes(BaseResource):

    url = '/events/types/'

    data_schema = {
        Required('lang'): All(unicode),
    }

    validators = [
        AuthRequiredValidator(),
    ]

    def get(self):

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
