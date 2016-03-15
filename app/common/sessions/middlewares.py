# -*- coding: utf-8 -*-

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
        session = SessionManager.get_session(session_id) if session_id else SessionManager.create_session()

        setattr(resource, 'session', session)

    def process_response(self, req, resp, resource):

        if not resource:
            return

        session = getattr(resource, 'session')
        if not session:
            return

        SessionManager.save_session(session)
        setattr(resource, 'session', None)

        resp.set_cookie(app_settings.SESSION_COOKIE_NAME, session.id, secure=False)
