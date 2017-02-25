# -*- coding: utf-8 -*-

from __future__ import absolute_import

from voluptuous import Required, All, Optional, Schema, Upper, In

from accounts.validators import AuthRequiredValidator
from core.exceptions import UserIsNotEventParticipant, AssigneeNotFoundException
from core.resources.base import BaseResource
from core.schemas import ListOf
from db.helpers import db_session
from events.logic import calculate_event_status
from events.models import Assignee
from events.permissions import PERMISSION
from events.validators import EventExistenceValidator, AccountIsEventParticipantValidator, StepExistenceValidator, \
    UpdateAssigneesValidator, getEventParticipant, PermissionValidator


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