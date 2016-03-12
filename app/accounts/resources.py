# -*- coding: utf-8 -*-

from facepy import GraphAPI, FacepyError, get_extended_access_token
from voluptuous import Required, All

from accounts.models import Account
from common.exceptions import FacebookLoginException
from common.resources.base import BaseResource
from common.sessions.models import SessionManager
from db.helpers import db_session

import settings as app_settings


__all__ = (
    'AuthFacebook',
)


class AuthFacebook(BaseResource):

    url = '/accounts/auth/facebook/'

    data_schema = {
        Required('user_access_token'): All(str),
    }

    validators = []

    def get(self, *args, **kwargs):

        if self.session:
            SessionManager.delete_session(self.session)

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
            account = db.query(Account).filter_by(identifier=str(fb_id), auth_method=app_settings.AUTH_FB).first()

            if not account:
                account = Account(name=fb_name,
                                  identifier=str(fb_id),
                                  auth_method=app_settings.AUTH_FB,
                                  attributes=fb_account
                                  )

            account.attributes['user_access_token'] = long_term_user_access_token
            account.attributes['expire_at'] = str(expire_at)
            db.merge(account)

        self.session = SessionManager.create_session()
        self.session['account_info'] = {'account_id': account.id}

        self.response_data = {
            'user_access_token': long_term_user_access_token,
            'session_id': self.session.id,
        }
