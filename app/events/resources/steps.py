# -*- coding: utf-8 -*-

from __future__ import absolute_import

from voluptuous import Required, All, Length, Optional, Upper, In, Schema

from accounts.validators import AuthRequiredValidator
from core.resources.base import BaseResource
from core.schemas import ListOf
from db.helpers import db_session
from events import Step
from events.logic import calculate_event_status
from events.permissions import PERMISSION
from events.validators import EventExistenceValidator, AccountIsEventParticipantValidator, PermissionValidator, \
    StepExistenceValidator, ChangeStepsOrderValidator


class CreateStep(BaseResource):

    url = '/v1/steps/create/'

    data_schema = {
        Required('event_id'): All(int),
        Required('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('type', default=Step.TYPE.CUSTOM): All(Upper, In(Step.TYPE.ALL)),
        Optional('order'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.CREATE_EVENT_STEP, ])
    ]

    def post(self):

        event = self.data.get('event')
        order = self.get_param('order')

        with db_session() as db:
            if order is None:
                if event.steps:
                    order = max(s.order for s in event.steps) + 1
                else:
                    order = 1
            step = Step(
                title=self.get_param('title'),
                description=self.get_param('description'),
                type=self.get_param('type'),
                event=event,
                order=order,
            )
            db.add(step)

        calculate_event_status.delay(event.id)

        self.response_data = {
            'step_id': step.id,
            'order': order,
        }


class UpdateStep(BaseResource):

    url = '/v1/steps/update/'

    data_schema = {
        Required('event_id'): All(int),
        Required('step_id'): All(int),
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('order'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UPDATE_EVENT_STEP, ]),
        StepExistenceValidator(),
    ]

    def post(self):

        step = self.data.get('step')

        title = self.get_param('title')
        description = self.get_param('description')
        order = self.get_param('order')

        if title:
            step.title = title

        if description:
            step.description = description

        if order:
            step.order = order

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

    def post(self):

        step = self.data.get('step')

        step_data = {
            'id': step.id,
            'title': step.title,
            'description': step.description,
            'type': step.type,
            'order': step.order,
            'assignees': [],
        }

        for assignee in step.assignees:
            step_data['assignees'].append({
                'participant_id': assignee.participant_id,
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
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT_STEP, ]),
        StepExistenceValidator(),
    ]

    def post(self):

        step = self.data.get('step')

        with db_session() as db:
            db.delete(step)

        calculate_event_status.delay(self.get_param('event_id'))

        self.response_data = {}


class ChangeStepsOrder(BaseResource):

    url = '/v1/steps/order/'

    step_order_schema = Schema({Required('id'): All(int), Required('order'): All(int)})

    data_schema = {
        Required('event_id'): All(int),
        Required('orders'): ListOf(step_order_schema),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.REORDER_EVENT_STEPS, ]),
        ChangeStepsOrderValidator()
    ]

    def post(self):

        steps = self.data.get('steps')

        with db_session() as db:
            for step, order in steps:
                step.order = order
                db.merge(step)

        self.response_data = {}
