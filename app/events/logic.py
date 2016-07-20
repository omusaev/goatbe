# -*- coding: utf-8 -*-

from sqlalchemy.orm import joinedload

from db.helpers import db_session
from events.models import Event, Assignee
from management import task

__all__ = (
    'calculate_event_status',
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
