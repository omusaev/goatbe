# -*- coding: utf-8 -*-

import requests

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


def create_anonym(args):
    url = '%s%s:%s/%s/accounts/auth/anonym/' % (SCHEMA, args.host, args.port, VER)
    response = requests.post(url)

    check_response(response)

    data = response.json()

    print 'Access token: %s' % data.get('data', {}).get('user_access_token')
    print 'Account_id: %s' % data.get('data', {}).get('account_id')
    print 'Session id: %s' % response.cookies.get('sessionid')

    if args.save:
        with open(SESSION_FILE, 'w') as session_file:
            session_file.write(response.cookies.get('sessionid'))


def auth_anonym(args):
    url = '%s%s:%s/%s/accounts/auth/anonym/' % (SCHEMA, args.host, args.port, VER)
    response = requests.post(url, json={'user_access_token': args.token})

    check_response(response)

    data = response.json()

    print 'Access token: %s' % data.get('data', {}).get('user_access_token')
    print 'Account_id: %s' % data.get('data', {}).get('account_id')
    print 'Session id: %s' % response.cookies.get('sessionid')

    if args.save:
        with open(SESSION_FILE, 'w') as session_file:
            session_file.write(response.cookies.get('sessionid'))


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-H', '--host', help='host', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='port', default='8000')

    sub_parsers = parser.add_subparsers()

    create_anonym_parser = sub_parsers.add_parser('create_anonym')
    create_anonym_parser.add_argument('-s', '--save', help='Save session id cookie to use in future requests')
    create_anonym_parser.set_defaults(handler='create_anonym')

    auth_anonym_parser = sub_parsers.add_parser('auth_anonym')
    auth_anonym_parser.add_argument('token')
    auth_anonym_parser.add_argument('-s', '--save', help='Save session id cookie to use in future requests', default=True)
    auth_anonym_parser.set_defaults(handler='auth_anonym')

    args = parser.parse_args()

    globals()[args.handler](args)

if __name__ in ('__main__',):
    main()
