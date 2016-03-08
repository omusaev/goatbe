# -*- coding: utf-8 -*-

from common.sessions.models import SessionManager

import settings as app_settings

__all__ = (
    'SessionMiddleware',
)


class SessionMiddleware(object):

    def process_request(self, req, resp):
        """Process the request before routing it.

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """

    def process_resource(self, req, resp, resource):
        """Process the request after routing.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed. May be None if no route was found for
                the request.
        """

        if not resource:
            return

        session_id = req.cookies.get(app_settings.SESSION_COOKIE_NAME)
        session = SessionManager.get_session(session_id) if session_id else None

        setattr(resource, 'session', session)

    def process_response(self, req, resp, resource):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
        """

        if not resource:
            return

        session = getattr(resource, 'session')
        if not session:
            return

        SessionManager.save_session(session)
        setattr(resource, 'session', None)

        resp.set_cookie(app_settings.SESSION_COOKIE_NAME, session.id, secure=False)
