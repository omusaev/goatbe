# -*- coding: utf-8 -*-

import falcon

from common.helpers import collect_installed_resources
from accounts.middlewares import AccountMiddleware
from common.sessions.middlewares import SessionMiddleware

application = falcon.API(middleware=[SessionMiddleware(), AccountMiddleware(), ])

for resource in collect_installed_resources():
    application.add_route(resource.url, resource)

if __name__ in ('__main__',):
    from management import handle_cli

    handle_cli()
    exit()
