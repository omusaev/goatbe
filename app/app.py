# -*- coding: utf-8 -*-

import falcon

from helpers import collect_installed_resources

application = falcon.API()

for resource in collect_installed_resources():
    application.add_route(resource.url, resource)

if __name__ in ('__main__',):
    print 'coming soon'
    exit()