# -*- coding: utf-8 -*-

from accounts import settings as account_settings
from accounts.models import Account
from common.decorators import cached_property
from db.helpers import db_session


__all__ = (
    'AccountMiddleware',
    'AccountInfo',
)


class AccountInfo(object):

    _account_id = None

    def __init__(self, id):
        self._account_id = id

    @cached_property
    def account(self):
        with db_session() as db:
            account = db.query(Account).get(self.account_id)

        return account

    @property
    def account_id(self):
        return self._account_id

    @property
    def user_access_token(self):
        return self.account.attributes['user_access_token']


class AccountMiddleware(object):

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource):

        if not resource:
            return

        if account_settings.ACCOUNT_ID_SESSION_KEY in resource.session:
            account_info = AccountInfo(resource.session.get(account_settings.ACCOUNT_ID_SESSION_KEY))
        else:
            account_info = None

        resource.account_info = account_info

    def process_response(self, req, resp, resource):
        pass
