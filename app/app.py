# -*- coding: utf-8 -*-

import falcon

from common.helpers import collect_installed_resources, collect_middlewares

__all__ = (
    'application',
)


application = falcon.API(middleware=list(collect_middlewares()))

for resource in collect_installed_resources():
    application.add_route(resource.url, resource)

if __name__ in ('__main__',):
    from management import handle_cli

    handle_cli()
    exit()
