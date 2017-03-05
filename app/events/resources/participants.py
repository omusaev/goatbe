# -*- coding: utf-8 -*-

from __future__ import absolute_import

from voluptuous import Required, All, Lower, Length

from accounts.validators import AuthRequiredValidator
from core.resources.base import BaseResource
from db.helpers import db_session
from events.mixins import EventDetailsMixin
from events.models import Participant, Assignee
from events.permissions import PERMISSION
from events.validators import (EventExistenceValidator, AccountIsEventParticipantValidator,
                               PermissionValidator, EventSecretValidator, AccountIsNotEventParticipantValidator)


class CreateParticipantSelf(BaseResource, EventDetailsMixin):

    url = '/v1/participants/create/self'

    data_schema = {
        Required('secret'): All(unicode, Lower, Length(max=32)),
    }

    validators = [
        AuthRequiredValidator(),
        EventSecretValidator(),
        AccountIsNotEventParticipantValidator(),
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

        self.response_data = self.short_event_details()


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


class DeleteParticipantSelf(BaseResource):

    url = '/v1/participants/delete/self'

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


class ActivateParticipantSelf(BaseResource):

    url = '/v1/participants/activate/self'

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
