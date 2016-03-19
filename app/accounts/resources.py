# -*- coding: utf-8 -*-

import uuid

from facepy import GraphAPI, FacepyError, get_extended_access_token
from voluptuous import Required, Optional, All

from accounts import settings as account_settings
from accounts.models import Account
from common.exceptions import FacebookLoginException, AccountNotFoundException
from common.resources import BaseResource
from db.helpers import db_session

import settings as app_settings


__all__ = (
    'AuthFacebook',
    'AuthAnonym',
)


class AuthBaseResource(BaseResource):

    def get(self, *args, **kwargs):

        if self.account_info:  # the user has already authenticated
            self.response_data = {
                'user_access_token': self.account_info.user_access_token,
            }
        else:
            account = self._auth()

            if account:
                self.session[account_settings.ACCOUNT_ID_SESSION_KEY] = account.id
                self.response_data = {
                    'user_access_token': account.attributes['user_access_token'],
                }
            else:
                raise AccountNotFoundException

    def _auth(self):
        raise NotImplementedError


class AuthFacebook(AuthBaseResource):

    url = '/accounts/auth/facebook/'

    data_schema = {
        Required('user_access_token'): All(unicode),
    }

    def _auth(self):
        user_access_token = self.get_param('user_access_token')

        try:
            fb_auth = get_extended_access_token(
                access_token=user_access_token,
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
            account = db.query(Account).filter_by(identifier=str(fb_id), auth_method=Account.AUTH_METHOD.FB).first()

            if not account:
                account = Account(
                    name=fb_name,
                    identifier=str(fb_id),
                    auth_method=Account.AUTH_METHOD.FB,
                    attributes=fb_account
                )

            account.attributes['user_access_token'] = long_term_user_access_token
            account.attributes['expire_at'] = str(expire_at)
            account = db.merge(account)

        return account


class AuthAnonym(AuthBaseResource):

    url = '/accounts/auth/anonym/'

    data_schema = {
        Optional('user_access_token'): All(unicode),
    }

    def _auth(self):
        user_access_token = self.get_param('user_access_token')

        with db_session() as db:
            if user_access_token:
                account = db.query(Account).filter_by(identifier=user_access_token,
                                                      auth_method=Account.AUTH_METHOD.ANONYM).first()
            else:  # new user, let's register him
                user_access_token = uuid.uuid4().hex
                account = Account(
                    name=user_access_token,
                    identifier=user_access_token,
                    auth_method=Account.AUTH_METHOD.ANONYM,
                    attributes={'user_access_token': user_access_token}
                )
                account = db.merge(account)

        return account