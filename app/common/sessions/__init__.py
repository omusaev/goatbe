# -*- coding: utf-8 -*-

from accounts.models import Account
from db.helpers import db_session


__all__ = (
    'AccountInfo',
)


class AccountInfo(object):
    account = None

    def __init__(self, id):
        with db_session() as db:
            account = db.query(Account).get(id)

        self.account = account

    @property
    def id(self):
        return self.account.id

    @property
    def user_access_token(self):
        return self.account.attributes['user_access_token']
