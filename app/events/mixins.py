# -*- coding: utf-8 -*-

from sqlalchemy import inspect
from sqlalchemy.orm import joinedload

from core.helpers import to_timestamp
from db.helpers import db_session

from events.models import Event


class EventDetailsMixin(object):

    def short_event_details(self, event=None):

        if event is None:
            event = self.data.get('event')

        state = inspect(event)

        if set(['participants', 'places', 'steps']) & state.unloaded:
            with db_session() as db:
                event = db.query(Event).options(joinedload('*')).get(event.id)

        event_data = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'status': event.status,
            'start_at': to_timestamp(event.start_at),
            'finish_at': to_timestamp(event.finish_at),
            'secret': event.secret,
            'participants': [],
            'steps': [],
            'places': [],
            'plan_items': [],
        }

        for participant in event.participants:
            event_data['participants'].append({
                'id': participant.id,
                'account': {
                    'id': participant.account.id,
                    'name': participant.account.name,
                    'avatar_url': participant.account.avatar_url,
                },
                'status': participant.status,
                'permissions': participant.permissions,
                'is_owner': participant.is_owner,
            })

        for step in event.steps:
            full_step = {
                'id': step.id,
                'title': step.title,
                'description': step.description,
                'type': step.type,
                'order': step.order,
                'assignees': [],
            }

            for assignee in step.assignees:
                full_step['assignees'].append({
                    'participant_id': assignee.participant_id,
                    'resolution': assignee.resolution,
                })

            event_data['steps'].append(full_step)

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

        for plan_item in event.plan_items:
            plan_item_data = {
                'id': plan_item.id,
                'title': plan_item.title,
                'description': plan_item.description,
                'start_at': to_timestamp(plan_item.start_at),
                'finish_at': to_timestamp(plan_item.finish_at),
                'order': plan_item.order,
                'point': None
            }

            if plan_item.geom_point:
                plan_item_data['point'] = {
                    'lng': plan_item.lng,
                    'lat': plan_item.lat,
                }

            event_data['plan_items'].append(plan_item_data)

        return event_data
