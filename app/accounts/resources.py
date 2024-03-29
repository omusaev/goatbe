# -*- coding: utf-8 -*-

import uuid

from facepy import GraphAPI, FacepyError, get_extended_access_token
from voluptuous import Required, Optional, All

from accounts import settings as account_settings
from accounts.models import Account
from accounts.validators import AuthRequiredValidator, AuthMethodValidator

from core.sessions.models import SessionManager
from core.exceptions import (
    FacebookLoginException, AccountNotFoundException,
    AlreadyLoggedInException, InvalidAccountStateException
)
from core.resources.base import BaseResource

from db.helpers import db_session

from events.models import Participant

import settings as app_settings

__all__ = (
    'AuthFacebook',
    'AuthAnonym',
    'ReplaceAnonym',
    'Logout',
    'UpdateAccount',
)


class AuthBaseResource(BaseResource):

    def post(self, *args, **kwargs):

        if self.account_info:  # the user has already authenticated
            raise AlreadyLoggedInException
        else:
            account = self._auth()

            if account:
                self.session[account_settings.ACCOUNT_ID_SESSION_KEY] = account.id
                self.response_data = {
                    'user_access_token': account.attributes['user_access_token'],
                    'account_id': account.id,
                }
            else:
                raise AccountNotFoundException

    def _auth(self):
        raise NotImplementedError


class AuthFacebook(AuthBaseResource):

    url = '/v1/accounts/auth/facebook/'

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
                    avatar_url="https://graph.facebook.com/v2.7/%s/picture/?type=large" % fb_id,
                    auth_method=Account.AUTH_METHOD.FB,
                    attributes=fb_account
                )

            account.attributes['user_access_token'] = long_term_user_access_token
            account.attributes['expire_at'] = str(expire_at)
            account = db.merge(account)

        return account


class AuthAnonym(AuthBaseResource):

    url = '/v1/accounts/auth/anonym/'

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


class ReplaceAnonym(BaseResource):

    url = '/v1/accounts/auth/anonym/replace/'

    data_schema = {
        Required('user_access_token'): All(unicode),
    }

    validators = [
        AuthRequiredValidator(),
        AuthMethodValidator(),
    ]

    def post(self, *args, **kwargs):

        user_access_token = self.get_param('user_access_token')

        with db_session() as db:
            anonym_account = db.query(Account).filter_by(identifier=user_access_token,
                                                         auth_method=Account.AUTH_METHOD.ANONYM).first()

        if not anonym_account:
            raise AccountNotFoundException

        account = self.account_info.account

        # We can create a validator to check that the account does not have events...
        # but it's too specific and won't be reused. So just put it right here!
        with db_session() as db:
            is_participant = bool(db.query(Participant).filter_by(account_id=account.id).count())

        if is_participant:
            raise InvalidAccountStateException

        # Ok, just replace anonym with normal account
        # todo: refactor swapping
        anonym_account.name = account.name
        anonym_account.status = account.status
        anonym_account.avatar_url = account.avatar_url
        anonym_account.auth_method = account.auth_method
        anonym_account.identifier = account.identifier
        anonym_account.attributes = account.attributes

        with db_session() as db:
            db.merge(anonym_account)
            db.query(Account).filter(Account.id == account.id).delete(synchronize_session=False)

        self.session[account_settings.ACCOUNT_ID_SESSION_KEY] = anonym_account.id


class Logout(BaseResource):

    url = '/v1/accounts/logout/'

    def post(self, *args, **kwargs):
        self.response_data = {}
        SessionManager.delete_session(self.session)
        self.session = None


class UpdateAccount(BaseResource):

    url = '/v1/accounts/update/'

    data_schema = {
        Optional('name'): All(unicode),
    }

    validators = [
        AuthRequiredValidator(),
    ]

    def post(self, *args, **kwargs):

        account = self.account_info.account

        name = self.get_param('name')

        if name:
            account.name = name

        with db_session() as db:
            db.merge(account)
