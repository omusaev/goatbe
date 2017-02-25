# -*- coding: utf-8 -*-

from core.helpers import to_timestamp

class EventShortDetailsMixin(object):

    def get_event_details(self):

        event = self.data.get('event')

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
