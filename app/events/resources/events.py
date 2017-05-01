# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime

from voluptuous import Required, All, Length, Optional, Upper, In

from accounts.validators import AuthRequiredValidator
from core.helpers import to_timestamp, to_datetime
from core.resources.base import BaseResource
from db.helpers import db_session
from events import EVENT_TYPES_DESCRIPTION
from events.mixins import EventDetailsMixin
from events.models import Participant, Event, Step
from events.permissions import PERMISSION
from events.validators import timestamp_validator, EventExistenceValidator, AccountIsEventParticipantValidator, \
    PermissionValidator, EventFinishedManuallyValidator


class EventTypes(BaseResource):

    url = '/v1/events/types/'

    data_schema = {
        Required('lang'): All(unicode),
    }

    validators = [
        AuthRequiredValidator(),
    ]

    def post(self):

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


class CreateEvent(BaseResource, EventDetailsMixin):

    url = '/v1/events/create/'

    data_schema = {
        Required('lang'): All(unicode),
        Required('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Required('start_at'): All(timestamp_validator),
        Required('finish_at'): All(timestamp_validator),
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
                    order=predefined_step.get('order'),
                )
                db.add(step)

            participant = Participant(
                account=account,
                event=event,
                is_owner=True,
                permissions=PERMISSION.DEFAULT_OWNER_SET,
            )
            db.add(participant)

        self.data['event'] = event
        self.response_data = self.short_event_details()


class UpdateEvent(BaseResource):

    url = '/v1/events/update/'

    data_schema = {
        Required('event_id'): All(int),
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('start_at'): All(timestamp_validator),
        Optional('finish_at'): All(timestamp_validator),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UPDATE_EVENT_DETAILS, ])
    ]

    def post(self):

        event = self.data.get('event')

        title = self.get_param('title')
        description = self.get_param('description')
        start_at = self.get_param('start_at')
        finish_at = self.get_param('finish_at')

        if title:
            event.title = title

        if description:
            event.description = description

        if start_at:
            event.start_at = start_at

        if finish_at:
            event.finish_at = finish_at

        with db_session() as db:
            db.merge(event)

        self.response_data = {}


class CancelEvent(BaseResource):

    url = '/v1/events/cancel/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(event_statuses=(Event.STATUS.PREPARATION, Event.STATUS.READY,
                                                Event.STATUS.IN_PROGRESS, Event.STATUS.NOT_COMPLETED)),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.CANCEL_EVENT, ])
    ]

    def post(self):

        event = self.data.get('event')

        event.attributes['precanceled_status'] = event.status
        event.status = Event.STATUS.CANCELED

        with db_session() as db:
            db.merge(event)

        self.response_data = {}


class RestoreEvent(BaseResource):

    url = '/v1/events/restore/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(event_statuses=(Event.STATUS.CANCELED, )),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.RESTORE_EVENT, ])
    ]

    def post(self):

        event = self.data.get('event')

        event.status = event.attributes.pop('precanceled_status')

        with db_session() as db:
            db.merge(event)

        self.response_data = {}


class FinishEvent(BaseResource):

    url = '/v1/events/finish/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(event_statuses=(Event.STATUS.PREPARATION, Event.STATUS.READY,
                                                Event.STATUS.IN_PROGRESS, Event.STATUS.NOT_COMPLETED)),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.FINISH_EVENT, ])
    ]

    def post(self):

        event = self.data.get('event')

        event.attributes['finished_manually'] = True
        event.attributes['prefinished_status'] = event.status
        event.attributes['prefinished_start_at'] = to_timestamp(event.start_at)
        event.attributes['prefinished_finish_at'] = to_timestamp(event.finish_at)
        event.status = Event.STATUS.FINISHED

        now = datetime.datetime.now()

        if event.finish_at > now:
            event.finish_at = now

            if event.start_at > event.finish_at:
                event.start_at = event.finish_at - datetime.timedelta(1)

        with db_session() as db:
            db.merge(event)

        self.response_data = {}


class UnfinishEvent(BaseResource):

    url = '/v1/events/unfinish/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(event_statuses=(Event.STATUS.FINISHED, )),
        EventFinishedManuallyValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UNFINISH_EVENT, ])
    ]

    def post(self):

        event = self.data.get('event')

        event.status = event.attributes.pop('prefinished_status')
        event.start_at = to_datetime(event.attributes.pop('prefinished_start_at'))
        event.finish_at = to_datetime(event.attributes.pop('prefinished_finish_at'))

        del event.attributes['finished_manually']

        with db_session() as db:
            db.merge(event)

        self.response_data = {}


class DeleteEvent(BaseResource):

    url = '/v1/events/delete/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT, ])
    ]

    def post(self):

        event = self.data.get('event')

        with db_session() as db:
            db.delete(event)

        self.response_data = {}


class ShortEventDetails(BaseResource, EventDetailsMixin):

    url = '/v1/events/details/short/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_SHORT_EVENT_DETAILS, ]),
    ]

    def post(self):
        self.response_data = self.short_event_details()


class EventList(BaseResource, EventDetailsMixin):

    url = '/v1/events/list/'

    validators = [
        AuthRequiredValidator(),
    ]

    def post(self):

        response_data = []
        account_id = self.account_info.account_id

        with db_session() as db:
            participants = db.query(Participant).filter_by(account_id=account_id)

            # TODO: add READ_SHORT_EVENT_DETAILS permission check
            for participant in participants:
                event = participant.event

                event_data = self.short_event_details(event=event)

                response_data.append(event_data)

        self.response_data = response_data


class EventDetails(BaseResource, EventDetailsMixin):

    url = '/v1/events/details/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_EVENT_DETAILS, ]),
    ]

    def post(self):
        # Now full details and short details are equal so short_event_details is used
        self.response_data = self.short_event_details()


class MapEventDetails(BaseResource):

    url = '/v1/events/details/map/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
    ]

    def post(self):

        event = self.data.get('event')

        event_data = {
            'title': event.title,
            'description': event.description,
            'status': event.status,
            'start_at': to_timestamp(event.start_at),
            'finish_at': to_timestamp(event.finish_at),
            'places': [],
        }

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

        self.response_data = event_data
