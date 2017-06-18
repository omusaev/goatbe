# -*- coding: utf-8 -*-

import datetime

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

        session = getattr(resource, 'session', None)

        if not session:
            resp.unset_cookie(app_settings.SESSION_COOKIE_NAME)
            return

        session.expire_at = datetime.datetime.now() + datetime.timedelta(seconds=app_settings.SESSION_TTL)

        SessionManager.save_session(session)

        resp.set_cookie(app_settings.SESSION_COOKIE_NAME, session.id,
                        max_age=app_settings.SESSION_TTL,
                        path=app_settings.SITE_PATH,
                        secure=False)
