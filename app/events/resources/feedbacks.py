# -*- coding: utf-8 -*-

from __future__ import absolute_import

from voluptuous import Required, All, Length, Optional

from accounts.validators import AuthRequiredValidator
from core.helpers import to_timestamp
from core.resources.base import BaseResource
from db.helpers import db_session
from events.models import Feedback
from events.permissions import PERMISSION
from events.validators import EventExistenceValidator, AccountIsEventParticipantValidator, PermissionValidator, \
    FeedbackExistenceValidator


class CreateFeedback(BaseResource):

    url = '/v1/feedbacks/create/'

    data_schema = {
        Required('event_id'): All(int),
        Required('comment'): All(unicode, Length(min=1, max=2000)),
        Optional('rating'): All(int),

    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.CREATE_EVENT_FEEDBACK, ])
    ]

    def post(self):

        account_id = self.account_info.account_id

        event = self.data.get('event')
        comment = self.get_param('comment')
        rating = self.get_param('rating')

        with db_session() as db:

            feedback = Feedback(
                comment=comment,
                rating=rating,
                event=event,
                account_id=account_id,
            )
            db.add(feedback)

        self.response_data = {
            'feedback_id': feedback.id,
        }


class UpdateFeedback(BaseResource):

    url = '/v1/feedbacks/update/'

    data_schema = {
        Required('event_id'): All(int),
        Optional('comment'): All(unicode, Length(min=1, max=2000)),
        Optional('rating'): All(int),

    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        FeedbackExistenceValidator(),
        PermissionValidator(
            permissions=[PERMISSION.UPDATE_ANOTHERS_EVENT_FEEDBACK, ],
            ownership={'entity': 'feedback'}
        )
    ]

    def post(self):

        feedback = self.data.get('feedback')

        comment = self.get_param('comment')
        rating = self.get_param('rating')

        if comment:
            feedback.comment = comment

        if rating:
            feedback.rating = rating

        with db_session() as db:
            db.merge(feedback)

        self.response_data = {}


class DeleteFeedback(BaseResource):

    url = '/v1/feedbacks/delete/'

    data_schema = {
        Required('event_id'): All(int),
        Required('feedback_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        (),
        PermissionValidator(
            permissions=[PERMISSION.DELETE_ANOTHERS_EVENT_FEEDBACK, ],
            ownership={'entity': 'feedback'}
        )
    ]

    def post(self):

        feedback = self.get_param('feedback')

        with db_session() as db:
            db.delete(feedback)

        self.response_data = {}


class FeedbackDetails(BaseResource):

    url = '/v1/feedbacks/details/'

    data_schema = {
        Required('event_id'): All(int),
        Required('feedback_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        FeedbackExistenceValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_EVENT_FEEDBACKS, ]),
    ]

    def post(self):

        feedback = self.data.get('feedback')

        feedback_data = {
            'id': feedback.id,
            'comment': feedback.comment,
            'rating': feedback.rating,
            'account_id': feedback.account_id,
            'created_at': to_timestamp(feedback.created_at),
        }

        self.response_data = feedback_data


class EventFeedbacks(BaseResource):

    url = '/v1/events/feedbacks/'

    data_schema = {
        Required('event_id'): All(int),
    }

    validators = [
        AuthRequiredValidator(),
        EventExistenceValidator(),
        AccountIsEventParticipantValidator(),
        PermissionValidator(permissions=[PERMISSION.READ_EVENT_FEEDBACKS, ]),
    ]

    def post(self):

        event = self.data.get('event')

        feedbacks_data = {
            'feedbacks': [],
        }

        for feedback in event.feedbacks:
            feedbacks_data['feedbacks'].append({
                'id': feedback.id,
                'comment': feedback.comment,
                'rating': feedback.rating,
                'account_id': feedback.account_id,
                'created_at': to_timestamp(feedback.created_at),
            })

        self.response_data = feedbacks_data