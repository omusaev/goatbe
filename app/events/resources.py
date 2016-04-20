# -*- coding: utf-8 -*-

from voluptuous import (
    Required, Optional, All, Length, Datetime, Upper, In
)

from accounts.validators import AuthRequiredValidator

from common.exceptions import AssigneeNotFoundException
from common.schemas import ListOf
from common.resources.base import BaseResource

from db.helpers import db_session

from events import EVENT_TYPES_DESCRIPTION, EVENT_DATES_FORMAT
from events.models import Event, Participant, Step, Assignee
from events.permissions import PERMISSION
from events.validators import (
    EventExistenceValidator, AccountIsEventParticipantValidator,
    StepExistenceValidator, PermissionValidator, UpdateAssigneesValidator
)

__all__ = (
    'EventTypes',
    'CreateEvent',
    'UpdateEvent',
    'CancelEvent',
    'RestoreEvent',
    'EventDetails',
    'EventList',

    'CreateStep',
    'UpdateStep',
    'StepDetails',
    'DeleteStep',

    'UpdateAssignees',
    'UpdateAssigneesResolution',
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
        Optional('destination'): All(unicode, Length(min=1, max=255)),
        Optional('start_at'): All(Datetime(format=EVENT_DATES_FORMAT)),
        Optional('finish_at'): All(Datetime(format=EVENT_DATES_FORMAT)),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(event_statuses=Event.STATUS.ALL_ACTIVE),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UPDATE_EVENT_DETAILS, ])
    ]

    def post(self):

        event = self.data.get('event')

        title = self.get_param('title')
        description = self.get_param('description')
        destination = self.get_param('destination')
        start_at = self.get_param('start_at')
        finish_at = self.get_param('finish_at')

        if title:
            event.title = title

        if description:
            event.description = description

        if destination:
            event.destination = destination

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
        EventExistenceValidator(event_statuses=Event.STATUS.ALL_ACTIVE),
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

        # todo: what status we have to set?! It's time to think about event status calculation mechanism...
        event.status = Event.STATUS.PREPARATION

        with db_session() as db:
            db.merge(event)

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
        PermissionValidator(permissions=[PERMISSION.READ_EVENT_DETAILS, ])
    ]

    def get(self):

        event = self.data.get('event')

        event_data = {
            'title': event.title,
            'destination': event.destination,
            'description': event.description,
            'status': event.status,
            'start_at': event.start_at.strftime(EVENT_DATES_FORMAT),
            'finish_at': event.finish_at.strftime(EVENT_DATES_FORMAT),
            'participants_count': len(event.participants),
            'participants': [],
            'steps': [],
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
        EventExistenceValidator(event_statuses=Event.STATUS.ALL_ACTIVE),
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
        EventExistenceValidator(event_statuses=Event.STATUS.ALL_ACTIVE),
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

    def get(self):

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
        EventExistenceValidator(event_statuses=Event.STATUS.ALL_ACTIVE),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT_STEP, ]),
        StepExistenceValidator(),
    ]

    def post(self):

        step_id = self.get_param('step_id')

        with db_session() as db:
            db.query(Assignee).filter(Assignee.step_id == step_id).delete(synchronize_session=False)
            db.query(Step).filter(Step.id == step_id).delete(synchronize_session=False)

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
        EventExistenceValidator(event_statuses=Event.STATUS.ALL_ACTIVE),
        AccountIsEventParticipantValidator(),
        StepExistenceValidator(),
        UpdateAssigneesValidator(),
    ]

    def post(self):

        step = self.data.get('step')

        with db_session() as db:

            for account_id in self.get_param('assign_accounts_ids'):
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

        self.response_data = {}


class UpdateAssigneesResolution(BaseResource):

    url = '/v1/assignees/resolution/update/'

    resolution_schema = {
        Required('account_id'): All(int),
        Required('resolution', default=Assignee.RESOLUTION.OPEN): All(Upper, In(Assignee.RESOLUTION.ALL)),
    }

    data_schema = {
        Required('event_id'): All(int),
        Required('step_id'): All(int),
        # TODO: not work. need fix.
        Required('resolutions'): ListOf(resolution_schema),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(event_statuses=Event.STATUS.ALL_ACTIVE),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UPDATE_STEP_RESOLUTION, ]),
        StepExistenceValidator(),
    ]

    def post(self):

        step_id = self.get_param('step_id')
        resolutions = self.get_param('resolutions')

        with db_session() as db:

            for item in resolutions:
                account_id = item.get('account_id')
                resolution = item.get('resolution')
                assignee = db.query(Assignee).filter_by(account_id=account_id, step_id=step_id).first()

                if not assignee:
                    raise AssigneeNotFoundException('Assignee with account_id %s from step %s was not found' % (account_id, step_id))

                assignee.resolution = resolution
                db.merge(assignee)

        self.response_data = {}
