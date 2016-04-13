# -*- coding: utf-8 -*-

from sqlalchemy.orm import joinedload

from common.exceptions import (
    EventNotFoundException, UserIsNotEventParticipant,
    StepNotFoundException, PermissionDeniedException,
    StepIsNotInEventException
)
from common.validators import BaseValidator
from db.helpers import db_session
from events.models import Event, Participant, Step

__all__ = (
    'EventExistenceValidator',
    'StepExistenceValidator',
    'AccountIsEventParticipantValidator',
    'PermissionValidator',
)


class EventExistenceValidator(BaseValidator):

    def run(self, resource, *args, **kwargs):
        event_id = resource.get_param('event_id')

        with db_session() as db:
            # todo: add is_deleted==false condition
            event = db.query(Event).options(joinedload('*')).get(event_id)

        if not event:
            raise EventNotFoundException

        resource.data['event'] = event


class StepExistenceValidator(BaseValidator):
    '''
    Needs EventExistenceValidator
    '''

    def run(self, resource, *args, **kwargs):
        step_id = resource.get_param('step_id')
        event = resource.data['event']

        with db_session() as db:
            step = db.query(Step).options(joinedload('*')).get(step_id)

        if not step:
            raise StepNotFoundException

        if step.event_id != event.id:
            raise StepIsNotInEventException

        resource.data['step'] = step


class AccountIsEventParticipantValidator(BaseValidator):
    '''
    Needs EventExistenceValidator
    '''

    def run(self, resource, *args, **kwargs):
        account_id = resource.account_info.account_id
        event = resource.data['event']

        with db_session() as db:
            participant = db.query(Participant).filter_by(account_id=account_id, event_id=event.id).first()

        if not participant:
            raise UserIsNotEventParticipant

        resource.data['participant'] = participant


class PermissionValidator(BaseValidator):
    '''
    Needs AccountIsEventParticipantValidator
    '''

    def __init__(self, permissions):
        self.permissions = permissions

    def run(self, resource, *args, **kwargs):
        participant = resource.data['participant']
        participant_permissions = participant.permissions

        if not set(self.permissions).issubset(set(participant_permissions)):
            raise PermissionDeniedException
