# -*- coding: utf-8 -*-

import requests

VER = 'v1'
SCHEMA = 'http://'


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


def unknown_command():
    print 'Unknown command\n'


def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('-H', '--host', help='host', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='port', default='8000')

    args = parser.parse_args()

    command = args.command

    {
        'create_anonym': create_anonym,
    }.get(command, unknown_command)(args)

if __name__ in ('__main__',):
    main()
