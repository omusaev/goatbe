# -*- coding: utf-8 -*-

from sqlalchemy import inspect
from sqlalchemy.orm import joinedload

from core.helpers import to_timestamp
from db.helpers import db_session

from events.models import Event


class EventDetailsMixin(object):

    def short_event_details(self):

        event = self.data.get('event')

        state = inspect(event)

        if set(['participants', 'places']) & state.unloaded:
            with db_session() as db:
                event = db.query(Event).options(joinedload('*')).get(event.id)
                self.data['event'] = event

        event_data = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'status': event.status,
            'start_at': to_timestamp(event.start_at),
            'finish_at': to_timestamp(event.finish_at),
            'secret': event.secret,
            'participants': [],
            'places': [],
        }

        for participant in event.participants:
            event_data['participants'].append({
                'account': {
                    'name': participant.account.name,
                    'avatar_url': participant.account.avatar_url,
                },
                'status': participant.status,
            })

        for place in event.places:
            event_data['places'].append({
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'start_at': to_timestamp(place.start_at),
                'finish_at': to_timestamp(place.finish_at),
                'order': place.order,
                'point': {
                    'lng': place.lng,
                    'lat': place.lat,
                }
            })

        return event_data
