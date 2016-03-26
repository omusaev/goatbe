# -*- coding: utf-8 -*-

import datetime

from common.sessions.models import SessionManager

import settings as app_settings

__all__ = (
    'SessionMiddleware',
)


class SessionMiddleware(object):

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource):

        if not resource:
            return

        session_id = req.cookies.get(app_settings.SESSION_COOKIE_NAME)
        session = SessionManager.get_or_create_session(session_id)

        resource.session = session

    def process_response(self, req, resp, resource):

        if not resource:
            return

        session = resource.session
        if not session:
            week_ago = datetime.datetime.now() - datetime.timedelta(7)
            resp.set_cookie(app_settings.SESSION_COOKIE_NAME, '', expires=week_ago, path=app_settings.SITE_PATH, secure=False)
            return

        SessionManager.save_session(session)

        resp.set_cookie(app_settings.SESSION_COOKIE_NAME, session.id, path=app_settings.SITE_PATH, secure=False)
