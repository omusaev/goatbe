# -*- coding: utf-8 -*-

if __name__ in ('__main__',):
    from management import handle_cli

    handle_cli()
    exit()
else:
    import falcon

    from core.helpers import collect_installed_resources, collect_middlewares

    application = falcon.API(middleware=list(collect_middlewares()))

    for resource in collect_installed_resources():
        application.add_route(resource.url, resource)
