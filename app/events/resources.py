# -*- coding: utf-8 -*-

from voluptuous import (
    Required, Optional, All, Length, Datetime, Upper, In, Schema
)

from accounts.validators import AuthRequiredValidator

from core.exceptions import AssigneeNotFoundException, UserIsNotEventParticipant
from core.schemas import ListOf
from core.resources.base import BaseResource

from db.helpers import db_session

from events import EVENT_TYPES_DESCRIPTION, EVENT_DATES_FORMAT
from events.logic import calculate_event_status
from events.models import Event, Participant, Step, Assignee, Place
from events.permissions import PERMISSION
from events.validators import (
    EventExistenceValidator, AccountIsEventParticipantValidator,
    StepExistenceValidator, PermissionValidator, UpdateAssigneesValidator,
    EventSecretValidator, PlaceExistenceValidator,
    getEventParticipant, TimestampValidator,
    ChangePlacesOrderValidator,
)

__all__ = (
    'EventTypes',
    'CreateEvent',
    'UpdateEvent',
    'CancelEvent',
    'RestoreEvent',
    'DeleteEvent',
    'LeaveEvent',
    'EventDetails',
    'ShortEventDetails',
    'ShortEventDetailsBySecret',
    'EventList',

    'DeleteParticipant',
    'CreateParticipant',
    'ActivateParticipant',

    'CreateStep',
    'UpdateStep',
    'StepDetails',
    'DeleteStep',

    'UpdateAssignees',
    'UpdateAssigneesResolution',

    'CreatePlace',
    'UpdatePlace',
    'DeletePlace',
    'PlaceDetails',
)


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


class CreateEvent(BaseResource):

    url = '/v1/events/create/'

    data_schema = {
        Required('lang'): All(unicode),
        Required('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
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


class UpdateEvent(BaseResource):

    url = '/v1/events/update/'

    data_schema = {
        Required('event_id'): All(int),
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('start_at'): All(Datetime(format=EVENT_DATES_FORMAT)),
        Optional('finish_at'): All(Datetime(format=EVENT_DATES_FORMAT)),
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
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.CANCEL_EVENT, ])
    ]

    def post(self):

        event = self.data.get('event')

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

        # todo: what status do we have to set?! It's time to think about event status calculation mechanism...
        event.status = Event.STATUS.PREPARATION

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


class LeaveEvent(BaseResource):

    url = '/v1/events/leave/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.LEAVE_EVENT, ])
    ]

    def post(self):

        event = self.data.get('event')
        account_id = self.account_info.account_id

        with db_session() as db:
            db.query(Participant).filter(Participant.account_id == account_id, Participant.event_id == event.id).delete(synchronize_session=False)

            for step in event.steps:
                db.query(Assignee).filter(Assignee.account_id == account_id, Assignee.step_id == step.id).delete(synchronize_session=False)

        self.response_data = {}


class EventDetails(BaseResource):

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

        event = self.data.get('event')

        event_data = {
            'title': event.title,
            'description': event.description,
            'status': event.status,
            'start_at': event.start_at.strftime(EVENT_DATES_FORMAT),
            'finish_at': event.finish_at.strftime(EVENT_DATES_FORMAT),
            'secret': event.secret,
            'participants': [],
            'steps': [],
            'places': [],
        }

        for participant in event.participants:
            event_data['participants'].append({
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
                'assignees': [],
            }

            for assignee in step.assignees:
                full_step['assignees'].append({
                    'account': {
                        'id': assignee.account.id,
                        'name': assignee.account.name,
                        'avatar_url': assignee.account.avatar_url,
                    },
                    'resolution': assignee.resolution,
                })

            event_data['steps'].append(full_step)

        for place in event.places:
            event_data['places'].append({
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'start_at': place.start_at,
                'finish_at': place.finish_at,
                'order': place.order,
                'point': {
                    'lng': place.lng,
                    'lat': place.lat,
                }
            })

        self.response_data = event_data


class ShortEventDetails(BaseResource):

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

        event = self.data.get('event')

        event_data = {
            'title': event.title,
            'description': event.description,
            'status': event.status,
            'start_at': event.start_at.strftime(EVENT_DATES_FORMAT),
            'finish_at': event.finish_at.strftime(EVENT_DATES_FORMAT),
            'participants': [],
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
                'start_at': place.start_at,
                'finish_at': place.finish_at,
                'order': place.order,
                'point': {
                    'lng': place.lng,
                    'lat': place.lat,
                }
            })

        self.response_data = event_data


class ShortEventDetailsBySecret(ShortEventDetails):

    url = '/v1/events/details/short/secret/'

    data_schema = {
        Required('event_id'): All(int),
        Required('event_secret'): All(unicode, Length(min=32, max=32)),
    }

    validators = [
        EventExistenceValidator(),
        EventSecretValidator(),
    ]


class EventList(BaseResource):

    url = '/v1/events/list/'

    validators = [
        AuthRequiredValidator(),
    ]

    def post(self):

        response_data = []
        account_id = self.account_info.account_id

        with db_session() as db:
            participants = db.query(Participant).filter_by(account_id=account_id)

            for participant in participants:
                event = participant.event

                event_data = {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'status': event.status,
                    'start_at': event.start_at.strftime(EVENT_DATES_FORMAT),
                    'finish_at': event.finish_at.strftime(EVENT_DATES_FORMAT),
                    'participant_status': participant.status,
                    'is_owner': participant.is_owner
                }

                response_data.append(event_data)

        self.response_data = response_data


class DeleteParticipant(BaseResource):

    url = '/v1/participants/delete/'

    data_schema = {
        Required('event_id'): All(int),
        Required('account_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT_PARTICIPANT, ])
    ]

    def post(self):

        event = self.data.get('event')
        account_id = self.get_param('account_id')

        with db_session() as db:
            db.query(Participant).filter(Participant.account_id == account_id, Participant.event_id == event.id).delete(synchronize_session=False)

            for step in event.steps:
                db.query(Assignee).filter(Assignee.account_id == account_id, Assignee.step_id == step.id).delete(synchronize_session=False)

        self.response_data = {}


class CreateParticipant(BaseResource):

    url = '/v1/participants/create/'

    data_schema = {
        Required('event_id'): All(int),
        Required('event_secret'): All(unicode, Length(min=32, max=32)),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        EventSecretValidator(),
    ]

    def post(self):

        event = self.data.get('event')
        account = self.account_info.account

        with db_session() as db:
            participant = Participant(
                account=account,
                event=event,
                is_owner=False,
                status=Participant.STATUS.INACTIVE,
                permissions=PERMISSION.DEFAULT_INACTIVE_SET,
            )
            db.merge(participant)

        self.response_data = {}


class ActivateParticipant(BaseResource):

    url = '/v1/participants/activate/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.ACTIVATE_EVENT_PARTICIPANT, ])
    ]

    def post(self):

        participant = self.data.get('participant')

        with db_session() as db:
            participant.permissions = PERMISSION.DEFAULT_NOT_OWNER_SET
            participant.status = Participant.STATUS.ACTIVE
            db.merge(participant)

        self.response_data = {}


class CreateStep(BaseResource):

    url = '/v1/steps/create/'

    data_schema = {
        Required('event_id'): All(int),
        Required('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('type', default=Step.TYPE.CUSTOM): All(Upper, In(Step.TYPE.ALL)),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.CREATE_EVENT_STEP, ])
    ]

    def post(self):

        event = self.data.get('event')

        with db_session() as db:
            step = Step(
                title=self.get_param('title'),
                description=self.get_param('description'),
                type=self.get_param('type'),
                event=event,
            )
            db.add(step)

        calculate_event_status.delay(event.id)

        self.response_data = {
            'step_id': step.id,
        }


class UpdateStep(BaseResource):

    url = '/v1/steps/update/'

    data_schema = {
        Required('event_id'): All(int),
        Required('step_id'): All(int),
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UPDATE_EVENT_STEP, ]),
        StepExistenceValidator(),
    ]

    def post(self):

        step = self.data.get('step')

        title = self.get_param('title')
        description = self.get_param('description')

        if title:
            step.title = title

        if description:
            step.description = description

        with db_session() as db:
            db.merge(step)

        self.response_data = {}


class StepDetails(BaseResource):

    url = '/v1/steps/details/'

    data_schema = {
        Required('event_id'): All(int),
        Required('step_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_STEP_DETAILS, ]),
        StepExistenceValidator(),
    ]

    def post(self):

        step = self.data.get('step')

        step_data = {
            'id': step.id,
            'title': step.title,
            'description': step.description,
            'type': step.type,
            'assignees': [],
        }

        for assignee in step.assignees:
            step_data['assignees'].append({
                'account': {
                    'id': assignee.account.id,
                    'name': assignee.account.name,
                    'avatar_url': assignee.account.avatar_url,
                },
                'resolution': assignee.resolution,
            })

        self.response_data = step_data


class DeleteStep(BaseResource):

    url = '/v1/steps/delete/'

    data_schema = {
        Required('event_id'): All(int),
        Required('step_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT_STEP, ]),
        StepExistenceValidator(),
    ]

    def post(self):

        step = self.get_param('step')

        with db_session() as db:
            db.delete(step)

        calculate_event_status.delay(self.get_param('event_id'))

        self.response_data = {}


class UpdateAssignees(BaseResource):

    url = '/v1/assignees/update/'

    data_schema = {
        Required('event_id'): All(int),
        Required('step_id'): All(int),
        Optional('assign_accounts_ids', default=[]): ListOf(int),
        Optional('unassign_accounts_ids', default=[]): ListOf(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        StepExistenceValidator(),
        UpdateAssigneesValidator(),
    ]

    def post(self):

        event = self.data.get('event')
        step = self.data.get('step')

        with db_session() as db:

            for account_id in self.get_param('assign_accounts_ids'):
                if not getEventParticipant(account_id=account_id, event_id=event.id):
                    msg = 'Account with id %s is not in event %s', (account_id, event.id)
                    raise UserIsNotEventParticipant(msg)

                assignee = db.query(Assignee).filter_by(account_id=account_id, step_id=step.id).first()

                if not assignee:
                    new_assignee = Assignee(
                        account_id=account_id,
                        step=step,
                    )
                    db.add(new_assignee)

            old_ids = self.get_param('unassign_accounts_ids')

            if old_ids:
                db.query(Assignee).filter(Assignee.account_id.in_(old_ids), Assignee.step_id == step.id).delete(synchronize_session=False)

        calculate_event_status.delay(event.id)

        self.response_data = {}


class UpdateAssigneesResolution(BaseResource):

    url = '/v1/assignees/resolution/update/'

    resolution_schema = Schema({
        Required('account_id'): All(int),
        Required('resolution', default=Assignee.RESOLUTION.OPEN): All(Upper, In(Assignee.RESOLUTION.ALL)),
    })

    data_schema = {
        Required('event_id'): All(int),
        Required('step_id'): All(int),
        Required('resolutions'): ListOf(resolution_schema),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UPDATE_STEP_RESOLUTION, ]),
        StepExistenceValidator(),
    ]

    def post(self):

        step = self.data.get('step')
        resolutions = self.get_param('resolutions')

        with db_session() as db:

            for item in resolutions:
                account_id = item.get('account_id')
                resolution = item.get('resolution')
                assignee = db.query(Assignee).filter_by(account_id=account_id, step_id=step.id).first()

                if not assignee:
                    raise AssigneeNotFoundException('Assignee with account_id %s from step %s was not found' % (account_id, step.id))

                assignee.resolution = resolution
                db.merge(assignee)

        calculate_event_status.delay(self.get_param('event_id'))

        self.response_data = {}


class CreatePlace(BaseResource):

    url = '/v1/places/create/'

    data_schema = {
        Required('event_id'): All(int),
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('start_at'): All(int, TimestampValidator()),
        Optional('finish_at'): All(int, TimestampValidator()),
        Required('order'): All(int),
        Required('point'): {
            Required('lng'): All(float),
            Required('lat'): All(float),
        },
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.CREATE_EVENT_PLACE, ])
    ]

    def post(self):

        event = self.data.get('event')

        with db_session() as db:
            place = Place(
                title=self.get_param('title'),
                description=self.get_param('description'),
                start_at=self.get_param('start_at'),
                finish_at=self.get_param('finish_at'),
                order=self.get_param('order'),
                point=Place.format_point(self.get_param('lng'), self.get_param('lat')),
                event=event,
            )
            db.add(place)

        self.response_data = {
            'place_id': place.id,
        }


class UpdatePlace(BaseResource):

    url = '/v1/places/update/'

    data_schema = {
        Required('event_id'): All(int),
        Required('place_id'): All(int),
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('start_at'): All(int, TimestampValidator()),
        Optional('finish_at'): All(int, TimestampValidator()),
        Optional('order'): All(int),
        Required('point'): {
            Optional('lng'): All(float),
            Optional('lat'): All(float),
        }
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UPDATE_EVENT_PLACE, ]),
        PlaceExistenceValidator(),
    ]

    def post(self):

        place = self.data.get('place')

        title = self.get_param('title')
        description = self.get_param('description')
        start_at = self.get_param('start_at')
        finish_at = self.get_param('finish_at')
        order = self.get_param('order')
        lng = self.get_param('lng')
        lat = self.get_param('lat')

        if title:
            place.title = title

        if description:
            place.description = description

        if start_at:
            place.start_at = start_at

        if finish_at:
            place.finish_at = finish_at

        if order:
            place.order = order

        if lng or lat:
            lng = lng or place.lng
            lat = lat or place.lat

            place.point = Place.format_point(lng, lat)

        with db_session() as db:
            db.merge(place)

        self.response_data = {}


class DeletePlace(BaseResource):

    url = '/v1/places/delete/'

    data_schema = {
        Required('event_id'): All(int),
        Required('place_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT_PLACE, ]),
        PlaceExistenceValidator(),
    ]

    def post(self):

        place = self.get_param('place')

        with db_session() as db:
            db.delete(place)

        self.response_data = {}


class PlaceDetails(BaseResource):

    url = '/v1/places/details/'

    data_schema = {
        Required('event_id'): All(int),
        Required('place_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_PLACE_DETAILS, ]),
        PlaceExistenceValidator(),
    ]

    def post(self):

        place = self.data.get('place')

        place_data = {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'start_at': place.start_at,
            'finish_at': place.finish_at,
            'order': place.order,
            'point': {
                'lng': place.lng,
                'lat': place.lat,
            }
        }

        self.response_data = place_data


class ChangePlacesOrder(BaseResource):

    url = '/v1/places/order/'

    place_order_schema = Schema({Required('id'): All(int), Required('order'): All(int)})

    data_schema = {
        Required('event_id'): All(int),
        Required('orders'): ListOf(place_order_schema),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.REORDER_EVENT_PLACE, ]),
        ChangePlacesOrderValidator()
    ]

    def post(self):

        places = self.data.get('places')

        with db_session() as db:
            for place, order in places:
                place.order = order
                db.merge(place)

        self.response_data = {}
