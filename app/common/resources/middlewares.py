# -*- coding: utf-8 -*-

__all__ = (
    'ResourceSetupMiddleware',
)


class ResourceSetupMiddleware(object):

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource):

        if not resource:
            return

        resource.request = req
        resource.response = resp

    def process_response(self, req, resp, resource):
        pass
