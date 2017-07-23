# -*- coding: utf-8 -*-

from __future__ import absolute_import

from voluptuous import Schema, Optional, All, Length, Required

from accounts.validators import AuthRequiredValidator
from core.helpers import to_timestamp
from core.resources.base import BaseResource
from core.schemas import ListOf
from db.helpers import db_session
from events.models import PlanItem
from events.permissions import PERMISSION
from events.validators import (timestamp_validator, EventExistenceValidator, AccountIsEventParticipantValidator,
                               PermissionValidator, PlanItemExistenceValidator, ChangePlanItemsOrderValidator)


# copy-paste from places
class CreatePlanItem(BaseResource):

    url = '/v1/plan_items/create/'

    plan_item_schema = Schema({
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('start_at'): All(timestamp_validator),
        Optional('finish_at'): All(timestamp_validator),
        Optional('order'): All(int),
        Optional('point'): {
            Required('lng'): All(float),
            Required('lat'): All(float),
        },
    })

    data_schema = {
        Required('event_id'): All(int),
        Required('plan_items'): ListOf(plan_item_schema),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.CREATE_EVENT_PLAN_ITEM, ])
    ]

    def post(self):

        event = self.data.get('event')
        plan_items = self.get_param('plan_items')

        with db_session() as db:

            new_plan_items = []

            for plan_item in plan_items:
                point = None
                
                if plan_item.get('point'):
                    lng = plan_item.get('point').get('lng')
                    lat = plan_item.get('point').get('lat')
                    point = PlanItem.format_point(lng, lat)

                new_plan_items.append(
                    PlanItem(
                        title=plan_item.get('title'),
                        description=plan_item.get('description'),
                        start_at=plan_item.get('start_at'),
                        finish_at=plan_item.get('finish_at'),
                        order=plan_item.get('order'),
                        point=point,
                        event=event,
                    )
                )

            db.add_all(new_plan_items)

        self.response_data = {
            'plan_items_ids': [p.id for p in new_plan_items],
        }


class UpdatePlanItem(BaseResource):

    url = '/v1/plan_items/update/'

    data_schema = {
        Required('event_id'): All(int),
        Required('plan_item_id'): All(int),
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('start_at'): All(timestamp_validator),
        Optional('finish_at'): All(timestamp_validator),
        Optional('order'): All(int),
        Optional('point'): {
            Required('lng'): All(float),
            Required('lat'): All(float),
        }
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.UPDATE_EVENT_PLAN_ITEM, ]),
        PlanItemExistenceValidator(),
    ]

    def post(self):

        plan_item = self.data.get('plan_item')

        title = self.get_param('title')
        description = self.get_param('description')
        start_at = self.get_param('start_at')
        finish_at = self.get_param('finish_at')
        order = self.get_param('order')
        point = self.get_param('point')

        if title:
            plan_item.title = title

        if description:
            plan_item.description = description

        if start_at:
            plan_item.start_at = start_at

        if finish_at:
            plan_item.finish_at = finish_at

        if order:
            plan_item.order = order

        if point:
            plan_item.point = PlanItem.format_point(point.get('lng'), point.get('lat'))

        with db_session() as db:
            db.merge(plan_item)

        self.response_data = {}


class DeletePlanItem(BaseResource):

    url = '/v1/plan_items/delete/'

    data_schema = {
        Required('event_id'): All(int),
        Required('plan_item_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT_PLAN_ITEM, ]),
        PlanItemExistenceValidator(),
    ]

    def post(self):

        plan_item = self.data.get('plan_item')

        with db_session() as db:
            db.delete(plan_item)

        self.response_data = {}


class PlanItemDetails(BaseResource):

    url = '/v1/plan_items/details/'

    data_schema = {
        Required('event_id'): All(int),
        Required('plan_item_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_PLAN_ITEM_DETAILS, ]),
        PlanItemExistenceValidator(),
    ]

    def post(self):

        plan_item = self.data.get('plan_item')

        plan_item_data = {
            'id': plan_item.id,
            'title': plan_item.title,
            'description': plan_item.description,
            'start_at': to_timestamp(plan_item.start_at),
            'finish_at': to_timestamp(plan_item.finish_at),
            'order': plan_item.order,
            'point': None
        }

        if plan_item.geom_point:
            plan_item_data['point'] = {
                'lng': plan_item.lng,
                'lat': plan_item.lat,
            }

        self.response_data = plan_item_data


class ChangePlanItemsOrder(BaseResource):

    url = '/v1/plan_items/order/'

    plan_item_order_schema = Schema({Required('id'): All(int), Required('order'): All(int)})

    data_schema = {
        Required('event_id'): All(int),
        Required('orders'): ListOf(plan_item_order_schema),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.REORDER_EVENT_PLAN_ITEMS, ]),
        ChangePlanItemsOrderValidator()
    ]

    def post(self):

        plan_items = self.data.get('plan_items')

        with db_session() as db:
            for plan_item, order in plan_items:
                plan_item.order = order
                db.merge(plan_item)

        self.response_data = {}
