# -*- coding: utf-8 -*-

import datetime
import fire
import pprint
import requests
import time

__all__ = (
    'GoatClient',
)


class GoatClient(object):

    _VER = 'v1'
    _SCHEMA = 'http://'
    _SESSION_FILE = './session'
    _SESSION_COOKIE_NAME = 'sessionid'

    def __init__(self, host='127.0.0.1', port='8000', quiet=False):
        self._host = host
        self._port = port
        self._quite = quiet

    def _out(self, msg):
        if not self._quite:
            pprint.pprint(msg)

    def _save_session_id(self, session_id):
        with open(self._SESSION_FILE, 'w') as session_file:
            session_file.write(session_id)

    def _load_session_id(self):
        try:
            with open(self._SESSION_FILE) as session_file:
                session_id = session_file.readlines()[0]
        except IOError:
            return None

        return session_id

    def flush_session(self, args):
        import os
        try:
            os.remove(self._SESSION_FILE)
        except OSError:
            return None

    def _url(self, uri):
        return '%s%s:%s/%s%s' % (self._SCHEMA, self._host, self._port, self._VER, uri)

    def _make_request(self, url, data, cookies=None, load_session=True):

        data = dict((k, v) for k, v in data.iteritems() if v is not None)

        if cookies is None:
            cookies = {}

        if load_session:
            session_id = self._load_session_id()
            cookies.update({self._SESSION_COOKIE_NAME: session_id})

        try:
            response = requests.post(url=url, json=data, cookies=cookies)
        except requests.exceptions.ConnectionError as e:
            self._out('Connection error: %s' % e)
            return

        self._check_response(response)
        self._output_response(response)

        return response

    def _check_response(self, response):

        if response.status_code not in (requests.codes.OK,):
            print 'Not OK http code: %s\n' % response.status_code
            exit(1)

        data = response.json()

        if data.get('status') not in ('ok',):
            print 'Not OK response status. Error_code: %s. Error_message: %s\n' % (
            data.get('error_code'), data.get('error_message'))
            exit(1)

    def _output_response(self, response):
        data = response.json()

        self._out(data.get('data'))

    def auth_anonym(self, user_access_token=None, save=True):
        url = self._url('/accounts/auth/anonym/')

        data = {'user_access_token': user_access_token}

        response = self._make_request(url, data)

        self._out('Session id: %s' % response.cookies.get('sessionid'))

        if save:
            self._save_session_id(response.cookies.get(self._SESSION_COOKIE_NAME))

        return response

    def auth_facebook(self, user_access_token, save=True):
        url = self._url('/accounts/auth/facebook/')

        data = {'user_access_token': user_access_token}

        response = self._make_request(url, data)

        self._out('Session id: %s' % response.cookies.get('sessionid'))

        if save:
            self._save_session_id(response.cookies.get(self._SESSION_COOKIE_NAME))

        return response

    def logout(self):
        url = self._url('/accounts/logout/')

        data = {}

        self._make_request(url, data)

    def events_types(self, lang='en'):
        url = self._url('/events/types/')

        data = {
            'lang': lang,
        }

        self._make_request(url, data)

    def create_event(self, title, description=None,
                     start_at=time.mktime(datetime.datetime.now().timetuple()),
                     finish_at=time.mktime((datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()),
                     event_type='hiking', lang='en'):
        url = self._url('/events/create/')

        data = {
            'lang': lang,
            'type': event_type,
            'title': title,
            'description': description,
            'start_at': start_at,
            'finish_at': finish_at,
        }

        self._make_request(url, data)

    def update_event(self, event_id, title, description=None, start_at=None, finish_at=None):
        url = self._url('/events/update/')

        data = {
            'event_id': event_id,
            'title': title,
            'description': description,
            'start_at': start_at,
            'finish_at': finish_at,
        }

        self._make_request(url, data)

    def event_details(self, event_id):
        url = self._url('/events/details/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def short_event_details(self, event_id):
        url = self._url('/events/details/short/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def event_list(self):
        url = self._url('/events/list/')

        data = {}

        self._make_request(url, data)

    def cancel_event(self, event_id):
        url = self._url('/events/cancel/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def restore_event(self, event_id):
        url = self._url('/events/restore/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def finish_event(self, event_id):
        url = self._url('/events/finish/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def unfinish_event(self, event_id):
        url = self._url('/events/unfinish/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def delete_event(self, event_id):
        url = self._url('/events/delete/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def map_event_details(self, event_id):
        url = self._url('/events/details/map/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def feedbacks_list(self, event_id):
        url = self._url('/feedbacks/list/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def create_feedback(self, event_id, comment, rating):
        url = self._url('/feedbacks/create/')

        data = {
            'event_id': event_id,
            'comment': comment,
            'rating': rating,
        }

        self._make_request(url, data)

    def update_feedback(self, event_id, feedback_id, comment, rating):
        url = self._url('/feedbacks/update/')

        data = {
            'event_id': event_id,
            'feedback_id': feedback_id,
            'comment': comment,
            'rating': rating,
        }

        self._make_request(url, data)

    def feedback_details(self, event_id, feedback_id):
        url = self._url('/feedbacks/details/')

        data = {
            'event_id': event_id,
            'feedback_id': feedback_id,
        }

        self._make_request(url, data)

    def delete_feedback(self, event_id, feedback_id):
        url = self._url('/feedbacks/delete/')

        data = {
            'event_id': event_id,
            'feedback_id': feedback_id,
        }

        self._make_request(url, data)

    def update_account(self, name):
        url = self._url('/accounts/update/')

        data = {
            'name': name,
        }

        self._make_request(url, data)

    def create_step(self, event_id, title, description=None, order=None, step_type='CUSTOM'):
        url = self._url('/steps/create/')

        data = {
            'event_id': event_id,
            'title': title,
            'description': description,
            'type': step_type,
            'order': order,
        }

        self._make_request(url, data)

    def update_step(self, event_id, step_id, title, description=None, order=None):
        url = self._url('/steps/update/')

        data = {
            'event_id': event_id,
            'step_id': step_id,
            'title': title,
            'description': description,
            'order': order,
        }

        self._make_request(url, data)

    def step_details(self, event_id, step_id):
        url = self._url('/steps/details/')

        data = {
            'event_id': event_id,
            'step_id': step_id,
        }

        self._make_request(url, data)

    def delete_step(self, event_id, step_id):
        url = self._url('/steps/delete/')

        data = {
            'event_id': event_id,
            'step_id': step_id,
        }

        self._make_request(url, data)

    def create_participant_self(self, secret):
        url = self._url('/participants/create/self/')

        data = {
            'secret': secret,
        }

        self._make_request(url, data)

    def activate_participant_self(self, event_id):
        url = self._url('/participants/activate/self/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def delete_participant(self, event_id, participant_id):
        url = self._url('/participants/delete/')

        data = {
            'event_id': event_id,
            'participant_id': participant_id,
        }

        self._make_request(url, data)

    def delete_participant_self(self, event_id):
        url = self._url('/participants/delete/self/')

        data = {
            'event_id': event_id,
        }

        self._make_request(url, data)

    def create_place(self, event_id, title, lng, lat,
                     description=None, order=None,
                     start_at=time.mktime(datetime.datetime.now().timetuple()),
                     finish_at=time.mktime((datetime.datetime.now() + datetime.timedelta(days=1)).timetuple())):
        url = self._url('/places/create/')

        data = {
            'event_id': event_id,
            'places': [
                {
                    'title': title,
                    'description': description,
                    'start_at': start_at,
                    'finish_at': finish_at,
                    'order': order,
                    'point': {
                        'lng': lng,
                        'lat': lat,
                    }
                },
            ]
        }

        self._make_request(url, data)

    def recreate_place(self, event_id, title, lng, lat,
                       description=None, order=None,
                       start_at=time.mktime(datetime.datetime.now().timetuple()),
                       finish_at=time.mktime((datetime.datetime.now() + datetime.timedelta(days=1)).timetuple())):
        url = self._url('/places/recreate/')

        data = {
            'event_id': event_id,
            'places': [
                {
                    'title': title,
                    'description': description,
                    'start_at': start_at,
                    'finish_at': finish_at,
                    'order': order,
                    'point': {
                        'lng': lng,
                        'lat': lat,
                    }
                },
            ]
        }

        self._make_request(url, data)

    def update_place(self, event_id, place_id, title=None, lng=None, lat=None,
                     description=None, order=None, start_at=None, finish_at=None):
        url = self._url('/places/update/')

        data = {
            'event_id': event_id,
            'place_id': place_id,
            'title': title,
            'description': description,
            'start_at': start_at,
            'finish_at': finish_at,
            'order': order,
            'point': {
                'lng': lng,
                'lat': lat,
            }
        }

        self._make_request(url, data)

    def place_details(self, event_id, place_id):
        url = self._url('/places/details/')

        data = {
            'event_id': event_id,
            'place_id': place_id,
        }

        self._make_request(url, data)

    def delete_place(self,  event_id, place_id):
        url = self._url('/places/delete/')

        data = {
            'event_id': event_id,
            'place_id': place_id,
        }

        self._make_request(url, data)

    def places_map(self):
        url = self._url('/places/map/')

        data = {}

        self._make_request(url, data)

    def update_assignees(self, event_id, step_id, assign_id, unassign_id=None):
        url = self._url('/assignees/update/')

        data = {
            'event_id': event_id,
            'step_id': step_id,
            'assign_participant_ids': [assign_id],
        }

        if unassign_id:
            data.update({
                'unassign_participant_ids': [unassign_id],
            })

        self._make_request(url, data)

    # TODO: add order steps
    # TODO: add order places


def main():
    fire.Fire(GoatClient)


if __name__ in ('__main__',):
    main()
