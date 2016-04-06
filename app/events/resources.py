# -*- coding: utf-8 -*-

from voluptuous import (
    Required, Optional, All, Length, Datetime, Upper, In
)

from accounts.validators import AuthRequiredValidator

from common.resources.base import BaseResource

from db.helpers import db_session

from events import EVENT_TYPES_DESCRIPTION, EVENT_DATES_FORMAT
from events.models import Event, Participant, Step, Assignee
from events.permissions import PERMISSION
from events.validators import EventExistenceValidator, AccountIsEventParticipantValidator, PermissionValidator

__all__ = (
    'EventTypes',
    'CreateEvent',
    'EventDetails',
    'EventList',
)


class EventTypes(BaseResource):

    url = '/v1/events/types/'

    data_schema = {
        Required('lang'): All(unicode),
    }

    validators = [
        AuthRequiredValidator(),
    ]

    def get(self):

        lang = self.get_param('lang')
        response_data = []

        # TODO: create admin panel
        for event_type, data in EVENT_TYPES_DESCRIPTION.iteritems():
            response_data.append({
                'type': event_type,
                'title': data.get(lang, {}).get('title'),
                'description': data.get(lang, {}).get('description'),
            })

        self.response_data = response_data


class CreateEvent(BaseResource):

    url = '/v1/events/create/'

    data_schema = {
        Required('lang'): All(unicode),
        Required('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('destination'): All(unicode, Length(min=1, max=255)),
        Required('start_at'): All(Datetime(format=EVENT_DATES_FORMAT)),
        Required('finish_at'): All(Datetime(format=EVENT_DATES_FORMAT)),
        Required('type'): All(Upper, In(Event.TYPE.ALL)),
    }

    validators = [
        AuthRequiredValidator(),
    ]

    def post(self):

        # todo: add lang validator or get lang from account attrs
        lang = self.get_param('lang')
        event_type = self.get_param('type')

        account = self.account_info.account

        with db_session() as db:
            event = Event(
                title=self.get_param('title'),
                description=self.get_param('description'),
                destination=self.get_param('destination'),
                start_at=self.get_param('start_at'),
                finish_at=self.get_param('finish_at'),
                type=event_type,
            )
            db.add(event)

            predefined_steps = EVENT_TYPES_DESCRIPTION.get(event_type, {}).get(lang, {}).get('steps', [])

            for predefined_step in predefined_steps:
                step = Step(
                    title=predefined_step.get('title'),
                    description=predefined_step.get('description'),
                    type=predefined_step.get('type'),
                    event=event,
                )
                db.add(step)

                assignee = Assignee(
                    account=account,
                    step=step,
                )
                db.add(assignee)

            participant = Participant(
                account=account,
                event=event,
                is_owner=True,
                permissions=PERMISSION.DEFAULT_OWNER_SET,
            )
            db.add(participant)

        self.response_data = {
            'event_id': event.id,
        }


class EventDetails(BaseResource):

    url = '/v1/events/details/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_EVENT_DETAILS,])
    ]

    def get(self):

        event = self.data['event']

        event_data = {
            'title': event.title,
            'destination': event.destination,
            'description': event.description,
            'status': event.status,
            'start_at': event.start_at.strftime(EVENT_DATES_FORMAT),
            'finish_at': event.finish_at.strftime(EVENT_DATES_FORMAT),
            'participants_count': len(event.participants),
        }

        event_data.update({'participants': []})

        for participant in event.participants:
            event_data['participants'].append({
                'account_id': participant.account_id,
                'status': participant.status,
                'permissions': participant.permissions,
                'is_owner': participant.is_owner,
            })

        event_data.update({'steps': []})

        for step in event.steps:
            full_step = {
                'title': step.title,
                'description': step.description,
                'type': step.type,
            }

            full_step.update({'assignees': []})

            for assignee in step.assignees:
                full_step['assignees'].append({
                    'account_id': assignee.account_id,
                    'resolution': assignee.resolution,
                })

            event_data['steps'].append(full_step)

        self.response_data = event_data


class EventList(BaseResource):

    url = '/v1/events/list/'

    validators = [
        AuthRequiredValidator(),
    ]

    def get(self):

        response_data = []
        account_id = self.account_info.account_id

        with db_session() as db:
            # todo: add deleted==false condition
            participants = db.query(Participant).filter_by(account_id=account_id)

            for participant in participants:
                event = participant.event

                event_data = {
                    'id': event.id,
                    'title': event.title,
                    'destination': event.destination,
                    'description': event.description,
                    'status': event.status,
                    'start_at': event.start_at.strftime(EVENT_DATES_FORMAT),
                    'finish_at': event.finish_at.strftime(EVENT_DATES_FORMAT),
                    'participant_status': participant.status,
                    'is_owner': participant.is_owner
                }

                response_data.append(event_data)

        self.response_data = response_data
