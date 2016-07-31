# -*- coding: utf-8 -*-

from core.sessions.models import SessionManager

import settings as app_settings

__all__ = (
    'SessionMiddleware',
)


class SessionMiddleware(object):

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource, params):
        session_id = req.cookies.get(app_settings.SESSION_COOKIE_NAME)
        session = SessionManager.get_or_create_session(session_id)

        resource.session = session

    def process_response(self, req, resp, resource):

        if not resource:
            return

        session = resource.session

        if not session:
            resp.unset_cookie(app_settings.SESSION_COOKIE_NAME)
            return

        SessionManager.save_session(session)

        resp.set_cookie(app_settings.SESSION_COOKIE_NAME, session.id, path=app_settings.SITE_PATH, secure=False)
