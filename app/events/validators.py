# -*- coding: utf-8 -*-

from sqlalchemy.orm import joinedload

from voluptuous import Invalid

from core.exceptions import (
    EventNotFoundException, UserIsNotEventParticipant,
    StepNotFoundException, PermissionDeniedException,
    StepIsNotInEventException, InvalidParameterException,
    InvalidEventStatusException, InvalidEventSecretException,
    PlaceNotFoundException, PlaceIsNotInEventException,
    EventIsNotFinishedManuallyException,
    FeedbackNotFoundException, FeedbackIsNotInEventException,
)
from core.helpers import to_datetime
from core.validators import BaseValidator
from db.helpers import db_session
from events.models import Event, Participant, Step, Place, Feedback
from events.permissions import PERMISSION

__all__ = (
    'timestamp_validator',
    'EventExistenceValidator',
    'StepExistenceValidator',
    'PlaceExistenceValidator',
    'AccountIsEventParticipantValidator',
    'PermissionValidator',
    'UpdateAssigneesValidator',
    'EventSecretValidator',
    'getEventParticipant',
    'ChangePlacesOrderValidator',
    'ChangeStepsOrderValidator',
    'EventFinishedManuallyValidator',
    'FeedbackExistenceValidator',
)


def timestamp_validator(timestamp):
    try:
        parsed = to_datetime(timestamp)
    except (ValueError, TypeError) as e:
        raise Invalid('Invalid timestamp', error_message=e.message)

    return parsed


class EventExistenceValidator(BaseValidator):

    def __init__(self, event_statuses=()):
        self.statuses = event_statuses

    def run(self, resource, *args, **kwargs):
        event_id = resource.get_param('event_id')

        with db_session() as db:
            event = db.query(Event).options(joinedload('*')).get(event_id)

        if not event:
            raise EventNotFoundException

        if self.statuses and event.status not in self.statuses:
            raise InvalidEventStatusException

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


class PlaceExistenceValidator(BaseValidator):
    '''
    Needs EventExistenceValidator
    '''

    def run(self, resource, *args, **kwargs):
        place_id = resource.get_param('place_id')
        event = resource.data['event']

        with db_session() as db:
            place = db.query(Place).options(joinedload('*')).get(place_id)

        if not place:
            raise PlaceNotFoundException

        if place.event_id != event.id:
            raise PlaceIsNotInEventException

        resource.data['place'] = place


class AccountIsEventParticipantValidator(BaseValidator):
    '''
    Needs EventExistenceValidator
    '''

    def run(self, resource, *args, **kwargs):
        account_id = resource.account_info.account_id
        event = resource.data['event']

        participant = getEventParticipant(account_id, event.id)

        if not participant:
            raise UserIsNotEventParticipant

        resource.data['participant'] = participant


class PermissionValidator(BaseValidator):
    '''
    Needs AccountIsEventParticipantValidator
    '''

    def __init__(self, permissions, ownership=None):
        self.permissions = permissions
        self.ownership = ownership

    def run(self, resource, *args, **kwargs):
        participant = resource.data['participant']
        participant_permissions = participant.permissions

        # check ownership condition. Owner can do all he wants with the object
        if self.ownership is not None:
            entity_name = self.ownership.get('entity')

            account_id = resource.account_info.account_id
            entity = resource.data[entity_name]

            if getattr(entity, 'account_id') == account_id:
                return

        if not set(self.permissions).issubset(set(participant_permissions)):
            raise PermissionDeniedException


class UpdateAssigneesValidator(BaseValidator):
    '''
    Needs AccountIsEventParticipantValidator
    '''

    def run(self, resource, *args, **kwargs):

        new_ids = resource.get_param('assign_accounts_ids')
        old_ids = resource.get_param('unassign_accounts_ids')

        if new_ids and old_ids and set(new_ids) & set(old_ids):
            raise InvalidParameterException('assign_accounts_ids and unassign_accounts_ids have core ids')

        if new_ids:
            # TODO: do not use other validators
            PermissionValidator(permissions=[PERMISSION.CREATE_STEP_ASSIGNEE, ]).run(resource, *args, **kwargs)

            event = resource.data.get('event')

            with db_session() as db:
                # TODO: only ACTIVE participants
                participants_count = db.query(Participant).filter(Participant.account_id.in_(new_ids), Participant.event_id == event.id).count()
                if participants_count != len(new_ids):
                    raise InvalidParameterException('Some of assign_accounts_ids not in event')

        if old_ids:
            PermissionValidator(permissions=[PERMISSION.DELETE_STEP_ASSIGNEE, ]).run(resource, *args, **kwargs)


class EventSecretValidator(BaseValidator):
    '''
    Needs EventExistenceValidator
    '''

    def run(self, resource, *args, **kwargs):

        event = resource.data['event']
        secret = resource.get_param('event_secret')

        if event.secret != secret:
            raise InvalidEventSecretException()


# TODO: codestyle. Move to the logic.py
def getEventParticipant(account_id, event_id):

    with db_session() as db:
        participant = db.query(Participant).filter_by(account_id=account_id, event_id=event_id).first()

    return participant or None


class ChangePlacesOrderValidator(BaseValidator):

    def run(self, resource, *args, **kwargs):

        orders = resource.get_param('orders')
        places = []

        for order_info in orders:
            place_id = order_info.get('id')
            order = order_info.get('order')

            with db_session() as db:
                place = db.query(Place).options(joinedload('*')).get(place_id)

            if not place:
                raise PlaceNotFoundException

            places.append((place, order, ))

        resource.data['places'] = places


class ChangeStepsOrderValidator(BaseValidator):

    def run(self, resource, *args, **kwargs):

        orders = resource.get_param('orders')
        steps = []

        for order_info in orders:
            step_id = order_info.get('id')
            order = order_info.get('order')

            with db_session() as db:
                step = db.query(Step).options(joinedload('*')).get(step_id)

            if not step:
                raise StepNotFoundException

            steps.append((step, order, ))

        resource.data['steps'] = steps


class EventFinishedManuallyValidator(BaseValidator):
    '''
    Needs EventExistenceValidator
    '''

    def run(self, resource, *args, **kwargs):

        event = resource.data['event']
        finished_manually = event.attributes.get('finished_manually')

        if not finished_manually:
            raise EventIsNotFinishedManuallyException


class FeedbackExistenceValidator(BaseValidator):
    '''
    Needs EventExistenceValidator
    '''

    def run(self, resource, *args, **kwargs):
        feedback_id = resource.get_param('feedback_id')
        event = resource.data['event']

        with db_session() as db:
            feedback = db.query(Feedback).options(joinedload('*')).get(feedback_id)

        if not feedback:
            raise FeedbackNotFoundException

        if feedback.event_id != event.id:
            raise FeedbackIsNotInEventException

        resource.data['feedback'] = feedback
