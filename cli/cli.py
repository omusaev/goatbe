# -*- coding: utf-8 -*-

import datetime
import requests
import time

VER = 'v1'
SCHEMA = 'http://'
SESSION_FILE = './session'


def check_response(response):
    if response.status_code not in (requests.codes.OK, ):
        print 'Not OK http code: %s\n' % response.status_code
        exit()

    data = response.json()

    if data.get('status') not in ('ok', ):
        print 'Not OK response status. Error_code: %s. Error_message: %s\n' % (data.get('error_code'), data.get('error_message'))
        exit()


def save_session_id(session_id):
    with open(SESSION_FILE, 'w') as session_file:
        session_file.write(session_id)


def read_session_id():
    with open(SESSION_FILE) as session_file:
        session_id = session_file.readlines()[0]

    return session_id

###################################################################################

def create_anonym(args):
    url = '%s%s:%s/%s/accounts/auth/anonym/' % (SCHEMA, args.host, args.port, VER)
    response = requests.post(url)

    check_response(response)

    data = response.json()

    print 'Access token: %s' % data.get('data', {}).get('user_access_token')
    print 'Account_id: %s' % data.get('data', {}).get('account_id')
    print 'Session id: %s' % response.cookies.get('sessionid')

    if args.save:
        save_session_id(response.cookies.get('sessionid'))


def auth_anonym(args):
    url = '%s%s:%s/%s/accounts/auth/anonym/' % (SCHEMA, args.host, args.port, VER)
    response = requests.post(url, json={'user_access_token': args.token})

    check_response(response)

    data = response.json()

    print 'Access token: %s' % data.get('data', {}).get('user_access_token')
    print 'Account_id: %s' % data.get('data', {}).get('account_id')
    print 'Session id: %s' % response.cookies.get('sessionid')

    if args.save:
        if args.save:
            save_session_id(response.cookies.get('sessionid'))


def create_event(args):
    url = '%s%s:%s/%s/events/create/' % (SCHEMA, args.host, args.port, VER)

    params = {
        'lang': args.lang,
        'type': args.type,
        'title': args.title,
        'description': args.description,
        'start_at': args.start_at,
        'finish_at': args.finish_at,
    }

    session_id=read_session_id()

    cookies = {'sessionid': session_id}

    response = requests.post(url, json=params, cookies=cookies)

    check_response(response)

    data = response.json()

    print 'Event id: %s' % data.get('data', {}).get('event_id')



def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-H', '--host', help='host', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='port', default='8000')

    sub_parsers = parser.add_subparsers()

    ##############################################################
    create_anonym_parser = sub_parsers.add_parser('create_anonym')

    create_anonym_parser.add_argument('-s', '--save', help='Save session id cookie to use in future requests')
    create_anonym_parser.set_defaults(handler='create_anonym')

    ##############################################################
    auth_anonym_parser = sub_parsers.add_parser('auth_anonym')

    auth_anonym_parser.add_argument('token')
    auth_anonym_parser.add_argument('-s', '--save', help='Save session id cookie to use in future requests', default=True)
    auth_anonym_parser.set_defaults(handler='auth_anonym')

    ##############################################################
    create_event_parser = sub_parsers.add_parser('create_event')

    create_event_parser.add_argument('--lang', default='en')
    create_event_parser.add_argument('--type', default='hiking')
    create_event_parser.add_argument('--title')
    create_event_parser.add_argument('--description')
    create_event_parser.add_argument('--start_at', default=time.mktime(datetime.datetime.now().timetuple()))
    create_event_parser.add_argument('--finish_at', default=time.mktime((datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()))

    create_event_parser.set_defaults(handler='create_event')


    args = parser.parse_args()

    globals()[args.handler](args)

if __name__ in ('__main__',):
    main()
