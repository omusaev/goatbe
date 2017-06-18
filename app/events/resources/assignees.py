# -*- coding: utf-8 -*-

from __future__ import absolute_import

from voluptuous import Required, All, Optional, Schema, Upper, In

from accounts.validators import AuthRequiredValidator
from core.exceptions import UserIsNotEventParticipant
from core.resources.base import BaseResource
from core.schemas import ListOf
from db.helpers import db_session
from events.logic import calculate_event_status, get_participant_by_id
from events.models import Assignee
from events.permissions import PERMISSION
from events.validators import EventExistenceValidator, AccountIsEventParticipantValidator, StepExistenceValidator, \
    PermissionValidator


class UpdateAssignees(BaseResource):

    url = '/v1/assignees/update/'

    data_schema = {
        Required('event_id'): All(int),
        Required('step_id'): All(int),
        Optional('assign_participant_ids', default=[]): ListOf(int),
        Optional('unassign_participant_ids', default=[]): ListOf(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        StepExistenceValidator(),
        PermissionValidator(permissions=[PERMISSION.CREATE_STEP_ASSIGNEE, PERMISSION.DELETE_STEP_ASSIGNEE]),
    ]

    def post(self):

        event = self.data.get('event')
        step = self.data.get('step')

        with db_session() as db:

            new_ids = self.get_param('assign_participant_ids')
            old_ids = self.get_param('unassign_participant_ids')
            all_ids = new_ids + old_ids

            for participant_id in all_ids:
                if not get_participant_by_id(participant_id, event.id):
                    msg = 'Participant with id %s is not in event %s', (participant_id, event.id)
                    raise UserIsNotEventParticipant(msg)

            for participant_id in new_ids:
                assignee = db.query(Assignee).filter_by(participant_id=participant_id, step_id=step.id).first()

                if not assignee:
                    new_assignee = Assignee(
                        participant_id=participant_id,
                        step=step,
                    )
                    db.add(new_assignee)

            if old_ids:
                db.query(Assignee).filter(Assignee.participant_id.in_(old_ids), Assignee.step_id == step.id).delete(synchronize_session=False)

        calculate_event_status.delay(event.id)

        self.response_data = {}


class UpdateAssigneesResolution(BaseResource):

    url = '/v1/assignees/resolution/update/'

    resolution_schema = Schema({
        Required('participant_id'): All(int),
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

        event = self.data.get('event')
        step = self.data.get('step')
        resolutions = self.get_param('resolutions')

        participant_ids = [item.get('participant_id') for item in resolutions]

        with db_session() as db:

            for participant_id in participant_ids:
                if not get_participant_by_id(participant_id, event.id):
                    msg = 'Participant with id %s is not in event %s', (participant_id, event.id)
                    raise UserIsNotEventParticipant(msg)

            for item in resolutions:
                participant_id = item.get('participant_id')
                resolution = item.get('resolution')
                assignee = db.query(Assignee).filter_by(participant_id=participant_id, step_id=step.id).first()

                if not assignee:
                    continue

                assignee.resolution = resolution
                db.merge(assignee)

        calculate_event_status.delay(self.get_param('event_id'))

        self.response_data = {}