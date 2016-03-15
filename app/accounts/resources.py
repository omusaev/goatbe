# -*- coding: utf-8 -*-

import uuid

from facepy import GraphAPI, FacepyError, get_extended_access_token
from voluptuous import Required, Optional, All

from accounts import settings as account_settings
from accounts.models import Account
from common.exceptions import FacebookLoginException
from common.resources.base import BaseResource
from db.helpers import db_session

import settings as app_settings


__all__ = (
    'AuthFacebook',
    'AuthAnonym',
)


class AuthBaseResource(BaseResource):

    account = None

    def get(self, *args, **kwargs):

        if self.account_info:  # the user has already authenticated
            self.response_data = {
                'user_access_token': self.account_info.user_access_token,
            }
        else:
            self._auth()
            self.session[account_settings.ACCOUNT_ID_SESSION_KEY] = self.account.id
            self.response_data = {
                'user_access_token': self.account.attributes['user_access_token'],
            }

    def _auth(self):
        raise NotImplementedError


class AuthFacebook(AuthBaseResource):

    url = '/accounts/auth/facebook/'

    data_schema = {
        Required('user_access_token'): All(str),
    }

    def _auth(self):
        user_access_token = self.request.get_param('user_access_token')

        try:
            fb_auth = get_extended_access_token(access_token=user_access_token,
                                                application_id=app_settings.FB_APP_ID,
                                                application_secret_key=app_settings.FB_APP_SECRET
                                                )
            graph = GraphAPI(oauth_token=fb_auth[0])
            fb_account = graph.get(path='/me')
        except FacepyError as e:
            raise FacebookLoginException(e.message)

        long_term_user_access_token = fb_auth[0]
        expire_at = fb_auth[1]

        fb_id = fb_account.get('id')
        fb_name = fb_account.get('name')

        with db_session() as db:
            self.account = db.query(Account).filter_by(identifier=str(fb_id),
                                                       auth_method=app_settings.AUTH_FB).first()

            if not self.account:
                self.account = Account(name=fb_name,
                                       identifier=str(fb_id),
                                       auth_method=app_settings.AUTH_FB,
                                       attributes=fb_account
                                       )

            self.account.attributes['user_access_token'] = long_term_user_access_token
            self.account.attributes['expire_at'] = str(expire_at)
            self.account = db.merge(self.account)


class AuthAnonym(AuthBaseResource):

    url = '/accounts/auth/anonym/'

    data_schema = {
        Optional('user_access_token'): All(str),
    }

    def _auth(self):
        user_access_token = self.request.get_param('user_access_token')

        with db_session() as db:
            if user_access_token:
                self.account = db.query(Account).filter_by(identifier=user_access_token,
                                                           auth_method=app_settings.AUTH_ANONYM).first()
            else:  # new user, let's register him
                user_access_token = uuid.uuid4().hex
                self.account = Account(name=user_access_token,
                                       identifier=user_access_token,
                                       auth_method=app_settings.AUTH_ANONYM,
                                       attributes={'user_access_token': user_access_token}
                                       )
                self.account = db.merge(self.account)
