# -*- coding: utf-8 -*-

from sqlalchemy.orm import joinedload

from common.exceptions import EventNotFoundException, UserIsNotEventParticipant
from common.validators import BaseValidator
from db.helpers import db_session
from events.models import Event, Participant

__all__ = (
    'EventExistenceValidator',
    'AccountIsEventParticipantValidator',
)


class EventExistenceValidator(BaseValidator):

    def run(self, resource, *args, **kwargs):
        event_id = resource.get_param('event_id')
        with db_session() as db:
            event = db.query(Event).options(joinedload('*')).get(event_id)

        if not event:
            raise EventNotFoundException

        resource.data['event'] = event


class AccountIsEventParticipantValidator(BaseValidator):

    def run(self, resource, *args, **kwargs):
        account_id = resource.account_info.account_id
        event = resource.data['event']

        with db_session() as db:
            participant = db.query(Participant).filter_by(account_id=account_id, event_id=event.id).first()

        if not participant:
            raise UserIsNotEventParticipant

        resource.data['participant'] = participant
