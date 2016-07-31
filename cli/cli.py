# -*- coding: utf-8 -*-

import datetime
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
            print msg

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
        os.remove(self.SESSION_FILE)

    def url(self, uri):
        return '%s%s:%s/%s%s' % (self.SCHEMA, self.host, self.port, self.VER, uri)

    def make_request(self, url, data, cookies=None, load_session=True):
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

    def create_anonym(self, args):
        url = self.url('/accounts/auth/anonym/')

        response = self.make_request(url, {})

        self.out('Session id: %s' % response.cookies.get('sessionid'))

        if args.save:
            self.save_session_id(response.cookies.get(self.SESSION_COOKIE_NAME))

        return response

    def auth_anonym(self, args):
        url = self.url('/accounts/auth/anonym/')

        data = {'user_access_token': args.token}

        response = self.make_request(url, data)

        self.out('Session id: %s' % response.cookies.get('sessionid'))

        if args.save:
            self.save_session_id(response.cookies.get(self.SESSION_COOKIE_NAME))

        return response

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

    def create_feedback(self, args):
        url = self.url('/feedbacks/create/')

        data = {
            'event_id': args.event,
            'comment': args.comment,
            'rating': args.rating,
        }

        return self.make_request(url, data)


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-H', '--host', help='host', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='port', default='8000')

    sub_parsers = parser.add_subparsers()

    #
    flush_session_parser = sub_parsers.add_parser('flush_session')
    flush_session_parser.set_defaults(handler='flush_session')

    #
    create_anonym_parser = sub_parsers.add_parser('create_anonym')

    create_anonym_parser.add_argument('-s', '--save', help='Save session id cookie to use in future requests', default=True)
    create_anonym_parser.set_defaults(handler='create_anonym')

    #
    auth_anonym_parser = sub_parsers.add_parser('auth_anonym')

    auth_anonym_parser.add_argument('token')
    auth_anonym_parser.add_argument('-s', '--save', help='Save session id cookie to use in future requests', default=True)
    auth_anonym_parser.set_defaults(handler='auth_anonym')

    #
    create_event_parser = sub_parsers.add_parser('create_event')

    create_event_parser.add_argument('--lang', default='en')
    create_event_parser.add_argument('--type', default='hiking')
    create_event_parser.add_argument('--title')
    create_event_parser.add_argument('--description')
    create_event_parser.add_argument('--start_at', default=time.mktime(datetime.datetime.now().timetuple()))
    create_event_parser.add_argument('--finish_at', default=time.mktime((datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()))

    create_event_parser.set_defaults(handler='create_event')

    #
    create_feedback_parser = sub_parsers.add_parser('create_feedback')

    create_feedback_parser.add_argument('--event', type=int)
    create_feedback_parser.add_argument('--comment')
    create_feedback_parser.add_argument('--rating', type=int)
    create_feedback_parser.set_defaults(handler='create_feedback')

    args = parser.parse_args()

    client = GoatClient(args.host, args.port)

    getattr(client, args.handler)(args)


if __name__ in ('__main__',):
    main()
