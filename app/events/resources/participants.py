# -*- coding: utf-8 -*-

from __future__ import absolute_import

from voluptuous import Required, All, Lower, Length

from accounts.validators import AuthRequiredValidator
from core.exceptions import UserIsNotEventParticipant
from core.resources.base import BaseResource
from db.helpers import db_session
from events.logic import get_participant_by_id
from events.mixins import EventDetailsMixin
from events.models import Participant
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
            )
            db.merge(participant)

        self.response_data = self.short_event_details()


class DeleteParticipant(BaseResource):

    url = '/v1/participants/delete/'

    data_schema = {
        Required('event_id'): All(int),
        Required('participant_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT_PARTICIPANT, ])
    ]

    def post(self):

        event = self.data.get('event')
        participant_id = self.get_param('participant_id')
        participant = get_participant_by_id(participant_id, event.id)

        if not participant:
            raise UserIsNotEventParticipant

        with db_session() as db:
            db.delete(participant)

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

        participant = self.data.get('participant')

        with db_session() as db:
            db.delete(participant)

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
