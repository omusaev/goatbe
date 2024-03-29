# -*- coding: utf-8 -*-

__all__ = (
    'ResourceSetupMiddleware',
)


class ResourceSetupMiddleware(object):

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource, params):
        resource._cleanup()

        resource.request = req
        resource.response = resp

        resource.data = {}

    def process_response(self, req, resp, resource):
        pass
