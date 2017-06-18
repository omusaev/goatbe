# -*- coding: utf-8 -*-

from sqlalchemy.orm import joinedload

from db.helpers import db_session
from events.models import Event, Assignee, Participant
from management import task

__all__ = (
    'is_step_resolved',
    'calculate_event_status',
    'get_participant_by_account_id',
    'get_participant_by_id',
)


def is_step_resolved(step):
    if not step.assignees:
        return False
    for assignee in step.assignees:
        if assignee.resolution == Assignee.RESOLUTION.OPEN:
            return False
    return True


@task
def calculate_event_status(event_id):
    with db_session() as db:
        event = db.query(Event).options(joinedload('*')).get(event_id)
        if event.is_finished():
            return

        if event.is_started():
            status = event.status
        else:
            status = Event.STATUS.PREPARATION

        for step in event.steps:
            if not is_step_resolved(step):
                break
        else:
            status = Event.STATUS.READY

        event.status = status
        db.merge(event)


def get_participant_by_account_id(account_id, event_id):

    with db_session() as db:
        participant = db.query(Participant).filter_by(account_id=account_id, event_id=event_id).first()

    return participant or None


def get_participant_by_id(id, event_id):

    with db_session() as db:
        participant = db.query(Participant).filter_by(id=id, event_id=event_id).first()

    return participant or None
