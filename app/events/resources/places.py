# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime

from voluptuous import Schema, Optional, All, Length, Required

from accounts.validators import AuthRequiredValidator
from core.helpers import to_timestamp
from core.resources.base import BaseResource
from core.schemas import ListOf
from db.helpers import db_session
from events import Event
from events.models import Place
from events.permissions import PERMISSION
from events.validators import timestamp_validator, EventExistenceValidator, AccountIsEventParticipantValidator, \
    PermissionValidator, PlaceExistenceValidator, ChangePlacesOrderValidator


class CreatePlace(BaseResource):

    url = '/v1/places/create/'

    place_schema = Schema({
        Optional('title'): All(unicode, Length(min=1, max=255)),
        Optional('description'): All(unicode, Length(min=1, max=2000)),
        Optional('start_at'): All(timestamp_validator),
        Optional('finish_at'): All(timestamp_validator),
        Optional('order'): All(int),
        Required('point'): {
            Required('lng'): All(float),
            Required('lat'): All(float),
        },
    })

    data_schema = {
        Required('event_id'): All(int),
        Required('places'): ListOf(place_schema),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.CREATE_EVENT_PLACE, ])
    ]

    def post(self):

        event = self.data.get('event')
        places = self.get_param('places')

        with db_session() as db:

            new_places = []

            for place in places:
                lng = place.get('point').get('lng')
                lat = place.get('point').get('lat')
                point = Place.format_point(lng, lat)

                new_places.append(
                    Place(
                        title=place.get('title'),
                        description=place.get('description'),
                        start_at=place.get('start_at'),
                        finish_at=place.get('finish_at'),
                        order=place.get('order'),
                        point=point,
                        event=event,
                    )
                )
                db.add_all(new_places)

        self.response_data = {
            'places_ids': [p.id for p in new_places],
        }


class UpdatePlace(BaseResource):

    url = '/v1/places/update/'

    data_schema = {
        Required('event_id'): All(int),
        Required('place_id'): All(int),
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
        PermissionValidator(permissions=[PERMISSION.UPDATE_EVENT_PLACE, ]),
        PlaceExistenceValidator(),
    ]

    def post(self):

        place = self.data.get('place')

        title = self.get_param('title')
        description = self.get_param('description')
        start_at = self.get_param('start_at')
        finish_at = self.get_param('finish_at')
        order = self.get_param('order')
        point = self.get_param('point')

        if title:
            place.title = title

        if description:
            place.description = description

        if start_at:
            place.start_at = start_at

        if finish_at:
            place.finish_at = finish_at

        if order:
            place.order = order

        if point:
            place.point = Place.format_point(point.get('lng'), point.get('lat'))

        with db_session() as db:
            db.merge(place)

        self.response_data = {}


class DeletePlace(BaseResource):

    url = '/v1/places/delete/'

    data_schema = {
        Required('event_id'): All(int),
        Required('place_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.DELETE_EVENT_PLACE, ]),
        PlaceExistenceValidator(),
    ]

    def post(self):

        place = self.get_param('place')

        with db_session() as db:
            db.delete(place)

        self.response_data = {}


class PlaceDetails(BaseResource):

    url = '/v1/places/details/'

    data_schema = {
        Required('event_id'): All(int),
        Required('place_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_PLACE_DETAILS, ]),
        PlaceExistenceValidator(),
    ]

    def post(self):

        place = self.data.get('place')

        place_data = {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'start_at': to_timestamp(place.start_at),
            'finish_at': to_timestamp(place.finish_at),
            'order': place.order,
            'point': {
                'lng': place.lng,
                'lat': place.lat,
            }
        }

        self.response_data = place_data


class ChangePlacesOrder(BaseResource):

    url = '/v1/places/order/'

    place_order_schema = Schema({Required('id'): All(int), Required('order'): All(int)})

    data_schema = {
        Required('event_id'): All(int),
        Required('orders'): ListOf(place_order_schema),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.REORDER_EVENT_PLACES, ]),
        ChangePlacesOrderValidator()
    ]

    def post(self):

        places = self.data.get('places')

        with db_session() as db:
            for place, order in places:
                place.order = order
                db.merge(place)

        self.response_data = {}


class MapPlaces(BaseResource):

    url = '/v1/places/map/'

    validators = [
        AuthRequiredValidator(),
    ]

    def post(self):

        response_data = []
        time_interval = 30

        after = datetime.datetime.now() - datetime.timedelta(time_interval)
        before = datetime.datetime.now() + datetime.timedelta(time_interval)

        with db_session() as db:
            places = db.query(Place).\
                outerjoin(Event, Place.event_id == Event.id).\
                filter(Event.finish_at > after, Event.start_at < before)

            for place in places:
                place_data = {
                    'id': place.id,
                    'title': place.title,
                    'description': place.description,
                    'start_at': to_timestamp(place.start_at),
                    'finish_at': to_timestamp(place.finish_at),
                    'point': {
                        'lng': place.lng,
                        'lat': place.lat,
                    },
                    'event_id': place.event_id,
                }

                response_data.append(place_data)

        self.response_data = response_data
