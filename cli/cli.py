# -*- coding: utf-8 -*-

import datetime
import pprint
import requests
import time

__all__ = (
    'GoatClient',
)


class GoatClient(object):

    VER = 'v1'
    SCHEMA = 'http://'
    SESSION_FILE = './session'
    SESSION_COOKIE_NAME = 'sessionid'

    def __init__(self, host, port, quiet=False):
        self.host = host
        self.port = port
        self.quite = quiet

    def out(self, msg):
        if not self.quite:
            pprint.pprint(msg)

    def save_session_id(self, session_id):
        with open(self.SESSION_FILE, 'w') as session_file:
            session_file.write(session_id)

    def load_session_id(self):
        try:
            with open(self.SESSION_FILE) as session_file:
                session_id = session_file.readlines()[0]
        except IOError:
            return None

        return session_id

    def flush_session(self, args):
        import os
        try:
            os.remove(self.SESSION_FILE)
        except OSError:
            return None

    def url(self, uri):
        return '%s%s:%s/%s%s' % (self.SCHEMA, self.host, self.port, self.VER, uri)

    def make_request(self, url, data, cookies=None, load_session=True):

        data = dict((k, v) for k, v in data.iteritems() if v is not None)

        if cookies is None:
            cookies = {}

        if load_session:
            session_id = self.load_session_id()
            cookies.update({self.SESSION_COOKIE_NAME: session_id})

        response = requests.post(url=url, json=data, cookies=cookies)

        self.check_response(response)
        self.output_response(response)

        return response

    def check_response(self, response):

        if response.status_code not in (requests.codes.OK,):
            print 'Not OK http code: %s\n' % response.status_code
            exit(1)

        data = response.json()

        if data.get('status') not in ('ok',):
            print 'Not OK response status. Error_code: %s. Error_message: %s\n' % (
            data.get('error_code'), data.get('error_message'))
            exit(1)

    def output_response(self, response):
        data = response.json()

        self.out(data.get('data'))

    def auth_anonym(self, args):
        url = self.url('/accounts/auth/anonym/')

        data = {'user_access_token': args.user_access_token}

        response = self.make_request(url, data)

        self.out('Session id: %s' % response.cookies.get('sessionid'))

        if args.save:
            self.save_session_id(response.cookies.get(self.SESSION_COOKIE_NAME))

        return response

    def auth_facebook(self, args):
        url = self.url('/accounts/auth/facebook/')

        data = {'user_access_token': args.user_access_token}

        response = self.make_request(url, data)

        self.out('Session id: %s' % response.cookies.get('sessionid'))

        if args.save:
            self.save_session_id(response.cookies.get(self.SESSION_COOKIE_NAME))

        return response

    def logout(self, args):
        url = self.url('/accounts/logout/')

        data = {}

        return self.make_request(url, data)

    def events_types(self, args):
        url = self.url('/events/types/')

        data = {
            'lang': args.lang,
        }

        return self.make_request(url, data)

    def create_event(self, args):
        url = self.url('/events/create/')

        data = {
            'lang': args.lang,
            'type': args.type,
            'title': args.title,
            'description': args.description,
            'start_at': args.start_at,
            'finish_at': args.finish_at,
        }

        return self.make_request(url, data)

    def update_event(self, args):
        url = self.url('/events/update/')

        data = {
            'event_id': args.event_id,
            'title': args.title,
            'description': args.description,
            'start_at': args.start_at,
            'finish_at': args.finish_at,
        }

        return self.make_request(url, data)

    def event_details(self, args):
        url = self.url('/events/details/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def short_event_details(self, args):
        url = self.url('/events/details/short/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def short_event_details_by_secret(self, args):
        url = self.url('/events/details/short/secret/')

        data = {
            'event_id': args.event_id,
            'event_secret': args.event_secret,
        }

        return self.make_request(url, data)

    def event_list(self, args):
        url = self.url('/events/list/')

        data = {}

        return self.make_request(url, data)

    def cancel_event(self, args):
        url = self.url('/events/cancel/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def restore_event(self, args):
        url = self.url('/events/restore/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def finish_event(self, args):
        url = self.url('/events/finish/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def unfinish_event(self, args):
        url = self.url('/events/unfinish/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def delete_event(self, args):
        url = self.url('/events/delete/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def leave_event(self, args):
        url = self.url('/events/leave/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def map_event_details(self, args):
        url = self.url('/events/details/map/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def event_feedbacks(self, args):
        url = self.url('/events/feedbacks/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def create_feedback(self, args):
        url = self.url('/feedbacks/create/')

        data = {
            'event_id': args.event_id,
            'comment': args.comment,
            'rating': args.rating,
        }

        return self.make_request(url, data)

    def update_feedback(self, args):
        url = self.url('/feedbacks/update/')

        data = {
            'event_id': args.event_id,
            'feedback_id': args.feedback_id,
            'comment': args.comment,
            'rating': args.rating,
        }

        return self.make_request(url, data)

    def feedback_details(self, args):
        url = self.url('/feedbacks/details/')

        data = {
            'event_id': args.event_id,
            'feedback_id': args.feedback_id,
        }

        return self.make_request(url, data)

    def delete_feedback(self, args):
        url = self.url('/feedbacks/delete/')

        data = {
            'event_id': args.event_id,
            'feedback_id': args.feedback_id,
        }

        return self.make_request(url, data)

    def update_account(self, args):
        url = self.url('/accounts/update/')

        data = {
            'name': args.name,
        }

        return self.make_request(url, data)

    def create_step(self, args):
        url = self.url('/steps/create/')

        data = {
            'event_id': args.event_id,
            'title': args.title,
            'description': args.description,
            'type': args.type,
            'order': args.order,
        }

        return self.make_request(url, data)

    def update_step(self, args):
        url = self.url('/steps/update/')

        data = {
            'event_id': args.event_id,
            'step_id': args.step_id,
            'title': args.title,
            'description': args.description,
            'order': args.order,
        }

        return self.make_request(url, data)

    def step_details(self, args):
        url = self.url('/steps/details/')

        data = {
            'event_id': args.event_id,
            'step_id': args.step_id,
        }

        return self.make_request(url, data)

    def delete_step(self, args):
        url = self.url('/steps/delete/')

        data = {
            'event_id': args.event_id,
            'step_id': args.step_id,
        }

        return self.make_request(url, data)

    def create_participant(self, args):
        url = self.url('/participants/create/')

        data = {
            'event_id': args.event_id,
            'event_secret': args.event_secret,
        }

        return self.make_request(url, data)

    def activate_participant(self, args):
        url = self.url('/participants/activate/')

        data = {
            'event_id': args.event_id,
        }

        return self.make_request(url, data)

    def delete_participant(self, args):
        url = self.url('/participants/delete/')

        data = {
            'event_id': args.event_id,
            'account_id': args.account_id,
        }

        return self.make_request(url, data)

    def create_place(self, args):
        url = self.url('/places/create/')

        data = {
            'event_id': args.event_id,
            'places': [
                {
                    'title': args.title,
                    'description': args.description,
                    'start_at': args.start_at,
                    'finish_at': args.finish_at,
                    'order': args.order,
                    'point': {
                        'lng': args.lng,
                        'lat': args.lat,
                    }
                },
            ]
        }

        return self.make_request(url, data)

    def update_place(self, args):
        url = self.url('/places/update/')

        data = {
            'event_id': args.event_id,
            'title': args.title,
            'description': args.description,
            'start_at': args.start_at,
            'finish_at': args.finish_at,
            'order': args.order,
            'point': {
                'lng': args.lng,
                'lat': args.lat,
            }
        }

        return self.make_request(url, data)

    def place_details(self, args):
        url = self.url('/places/details/')

        data = {
            'event_id': args.event_id,
            'place_id': args.place_id,
        }

        return self.make_request(url, data)

    def delete_place(self, args):
        url = self.url('/places/delete/')

        data = {
            'event_id': args.event_id,
            'place_id': args.place_id,
        }

        return self.make_request(url, data)

    def places_map(self, args):
        url = self.url('/places/map/')

        data = {}

        return self.make_request(url, data)


def add_event_parsers(sub_parsers):

    events_types_parser = sub_parsers.add_parser('events_types')
    events_types_parser.add_argument('--lang', default='en')
    events_types_parser.set_defaults(handler='events_types')

    create_event_parser = sub_parsers.add_parser('create_event')
    create_event_parser.add_argument('--lang', default='en')
    create_event_parser.add_argument('--type', default='hiking')
    create_event_parser.add_argument('--title')
    create_event_parser.add_argument('--description')
    create_event_parser.add_argument('--start_at', default=time.mktime(datetime.datetime.now().timetuple()))
    create_event_parser.add_argument('--finish_at', default=time.mktime(
        (datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()))
    create_event_parser.set_defaults(handler='create_event')

    update_event_parser = sub_parsers.add_parser('update_event')
    update_event_parser.add_argument('--event_id', type=int)
    update_event_parser.add_argument('--title')
    update_event_parser.add_argument('--description')
    update_event_parser.add_argument('--start_at', type=int)
    update_event_parser.add_argument('--finish_at', type=int)
    update_event_parser.set_defaults(handler='update_event')

    event_details_parser = sub_parsers.add_parser('event_details')
    event_details_parser.add_argument('--event_id', type=int)
    event_details_parser.set_defaults(handler='event_details')

    short_event_details_parser = sub_parsers.add_parser('short_event_details')
    short_event_details_parser.add_argument('--event_id', type=int)
    short_event_details_parser.set_defaults(handler='short_event_details')

    short_event_details_by_secret_parser = sub_parsers.add_parser('short_event_details_by_secret')
    short_event_details_by_secret_parser.add_argument('--event_id', type=int)
    short_event_details_by_secret_parser.add_argument('--event_secret')
    short_event_details_by_secret_parser.set_defaults(handler='short_event_details_by_secret')

    event_list_parser = sub_parsers.add_parser('event_list')
    event_list_parser.set_defaults(handler='event_list')

    cancel_event_parser = sub_parsers.add_parser('cancel_event')
    cancel_event_parser.add_argument('--event_id', type=int)
    cancel_event_parser.set_defaults(handler='cancel_event')

    restore_event_parser = sub_parsers.add_parser('restore_event')
    restore_event_parser.add_argument('--event_id', type=int)
    restore_event_parser.set_defaults(handler='restore_event')

    finish_event_parser = sub_parsers.add_parser('finish_event')
    finish_event_parser.add_argument('--event_id', type=int)
    finish_event_parser.set_defaults(handler='finish_event')

    unfinish_event_parser = sub_parsers.add_parser('unfinish_event')
    unfinish_event_parser.add_argument('--event_id', type=int)
    unfinish_event_parser.set_defaults(handler='unfinish_event')

    delete_event_parser = sub_parsers.add_parser('delete_event')
    delete_event_parser.add_argument('--event_id', type=int)
    delete_event_parser.set_defaults(handler='delete_event')

    leave_event_parser = sub_parsers.add_parser('leave_event')
    leave_event_parser.add_argument('--event_id', type=int)
    leave_event_parser.set_defaults(handler='leave_event')

    map_event_details_parser = sub_parsers.add_parser('map_event_details')
    map_event_details_parser.add_argument('--event_id', type=int)
    map_event_details_parser.set_defaults(handler='map_event_details')

    event_feedbacks_parser = sub_parsers.add_parser('event_feedbacks')
    event_feedbacks_parser.add_argument('--event_id', type=int)
    event_feedbacks_parser.set_defaults(handler='event_feedbacks')


def add_feedback_parsers(sub_parsers):

    create_feedback_parser = sub_parsers.add_parser('create_feedback')
    create_feedback_parser.add_argument('--event_id', type=int)
    create_feedback_parser.add_argument('--comment')
    create_feedback_parser.add_argument('--rating', type=int)
    create_feedback_parser.set_defaults(handler='create_feedback')

    update_feedback_parser = sub_parsers.add_parser('update_feedback')
    update_feedback_parser.add_argument('--event_id', type=int)
    update_feedback_parser.add_argument('--feedback_id', type=int)
    update_feedback_parser.add_argument('--comment')
    update_feedback_parser.add_argument('--rating', type=int)
    update_feedback_parser.set_defaults(handler='update_feedback')

    feedback_details_parser = sub_parsers.add_parser('feedback_details')
    feedback_details_parser.add_argument('--event_id', type=int)
    feedback_details_parser.add_argument('--feedback_id', type=int)
    feedback_details_parser.set_defaults(handler='feedback_details')

    delete_feedback_parser = sub_parsers.add_parser('delete_feedback')
    delete_feedback_parser.add_argument('--event_id', type=int)
    delete_feedback_parser.add_argument('--feedback_id', type=int)
    delete_feedback_parser.set_defaults(handler='delete_feedback')


def add_auth_parsers(sub_parsers):

    flush_session_parser = sub_parsers.add_parser('flush_session')
    flush_session_parser.set_defaults(handler='flush_session')

    auth_anonym_parser = sub_parsers.add_parser('auth_anonym')
    auth_anonym_parser.add_argument('user_access_token')
    auth_anonym_parser.add_argument('-s', '--save', help='Save session id cookie to use in future requests',
                                    default=True)
    auth_anonym_parser.set_defaults(handler='auth_anonym')

    auth_facebook_parser = sub_parsers.add_parser('auth_facebook')
    auth_facebook_parser.add_argument('user_access_token')
    auth_facebook_parser.add_argument('-s', '--save', help='Save session id cookie to use in future requests',
                                    default=True)
    auth_facebook_parser.set_defaults(handler='auth_facebook')

    logout_parser = sub_parsers.add_parser('logout_parser')
    logout_parser.set_defaults(handler='logout_parser')


def add_accounts_parsers(sub_parsers):

    update_account_parser = sub_parsers.add_parser('update_account')
    update_account_parser.add_argument('--name')
    update_account_parser.set_defaults(handler='update_account')


def add_step_parsers(sub_parsers):

    create_step_parser = sub_parsers.add_parser('create_step')
    create_step_parser.add_argument('--event_id', type=int)
    create_step_parser.add_argument('--type', default='CUSTOM')
    create_step_parser.add_argument('--title')
    create_step_parser.add_argument('--description')
    create_step_parser.add_argument('--order', type=int)
    create_step_parser.set_defaults(handler='create_step')

    update_step_parser = sub_parsers.add_parser('update_step')
    update_step_parser.add_argument('--event_id', type=int)
    update_step_parser.add_argument('--step_id', type=int)
    update_step_parser.add_argument('--title')
    update_step_parser.add_argument('--description')
    update_step_parser.add_argument('--order', type=int)
    update_step_parser.set_defaults(handler='update_step')

    step_details_parser = sub_parsers.add_parser('step_details')
    step_details_parser.add_argument('--event_id', type=int)
    step_details_parser.add_argument('--step_id', type=int)
    step_details_parser.set_defaults(handler='step_details')

    delete_step_parser = sub_parsers.add_parser('delete_step')
    delete_step_parser.add_argument('--event_id', type=int)
    delete_step_parser.add_argument('--step_id', type=int)
    delete_step_parser.set_defaults(handler='delete_step')


def add_participant_parsers(sub_parsers):

    create_participant_parser = sub_parsers.add_parser('create_participant')
    create_participant_parser.add_argument('--event_id', type=int)
    create_participant_parser.add_argument('--event_secret')
    create_participant_parser.set_defaults(handler='create_participant')

    activate_participant_parser = sub_parsers.add_parser('activate_participant')
    activate_participant_parser.add_argument('--event_id', type=int)
    activate_participant_parser.set_defaults(handler='activate_participant')

    delete_participant_parser = sub_parsers.add_parser('delete_participant')
    delete_participant_parser.add_argument('--event_id', type=int)
    delete_participant_parser.add_argument('--account_id', type=int)
    delete_participant_parser.set_defaults(handler='delete_participant')


def add_place_parsers(sub_parsers):

    create_place_parser = sub_parsers.add_parser('create_place')
    create_place_parser.add_argument('--event_id', type=int)
    create_place_parser.add_argument('--title')
    create_place_parser.add_argument('--description')
    create_place_parser.add_argument('--start_at', default=time.mktime(datetime.datetime.now().timetuple()))
    create_place_parser.add_argument('--finish_at', default=time.mktime(
        (datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()))
    create_place_parser.add_argument('--order', type=int)
    create_place_parser.add_argument('--lng', type=float)
    create_place_parser.add_argument('--lat', type=float)
    create_place_parser.set_defaults(handler='create_place')

    update_place_parser = sub_parsers.add_parser('update_place')
    update_place_parser.add_argument('--event_id', type=int)
    update_place_parser.add_argument('--title')
    update_place_parser.add_argument('--description')
    update_place_parser.add_argument('--start_at', default=time.mktime(datetime.datetime.now().timetuple()))
    update_place_parser.add_argument('--finish_at', default=time.mktime(
        (datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()))
    update_place_parser.add_argument('--order', type=int)
    update_place_parser.add_argument('--lng', type=float)
    update_place_parser.add_argument('--lat', type=float)
    update_place_parser.set_defaults(handler='update_place')

    place_details_parser = sub_parsers.add_parser('place_details')
    place_details_parser.add_argument('--event_id', type=int)
    place_details_parser.add_argument('--place_id', type=int)
    place_details_parser.set_defaults(handler='place_details')

    delete_place_parser = sub_parsers.add_parser('delete_place')
    delete_place_parser.add_argument('--event_id', type=int)
    delete_place_parser.add_argument('--place_id', type=int)
    delete_place_parser.set_defaults(handler='delete_place')

    places_map_parser = sub_parsers.add_parser('places_map')
    places_map_parser.set_defaults(handler='places_map')


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-H', '--host', help='host', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='port', default='8000')

    sub_parsers = parser.add_subparsers()

    add_auth_parsers(sub_parsers)
    add_event_parsers(sub_parsers)
    add_feedback_parsers(sub_parsers)
    add_accounts_parsers(sub_parsers)
    add_step_parsers(sub_parsers)
    add_participant_parsers(sub_parsers)
    add_place_parsers(sub_parsers)

    # TODO: add assignees parsers
    # TODO: add order steps
    # TODO: add order places

    args = parser.parse_args()

    client = GoatClient(args.host, args.port)

    getattr(client, args.handler)(args)


if __name__ in ('__main__',):
    main()
