# -*- coding: utf-8 -*-

import json

from voluptuous import (
    Schema, MultipleInvalid,
    RequiredFieldInvalid,
)

from common.exceptions import (
    GoatBaseException,
    UnsupportedResourceMethodException,
    MissingParameterException,
    InvalidParameterFormatException,
)

__all__ = (
    'BaseResource',
    'ResourceSetupMiddleware',
)


class BaseResource(object):

    url = None

    # data_schema describes data parameters and how to validate them.
    # Redefine it in child class if you want to change something
    #
    # There is an opportunity to add your custom format validator (see voluptuous docs).
    # But beware of complex inspections like a db query, or validation of related fields.
    data_schema = {}

    # Order matters! For example, to validate that the user has some permissions we firstly have to validate the user.
    validators = []

    def _cleanup(self):
        self.__dict__ = {}

    @property
    def url(self):
        return self.url

    def get_param(self, name, default=None):
        return self.params.get(name, default) if hasattr(self, 'params') else default

    def handle_request(self, req, resp, *args, **kwargs):
        """
        Common entry point. Prepares request, processes request and prepares response
        :param req:
        :param resp:
        :param args:
        :param kwargs:
        :return:
        """

        try:
            self.prepare_request(*args, **kwargs)
            self.process_request(*args, **kwargs)
        except GoatBaseException as e:
            self.raised_exception = e

        self.prepare_response()

    def process_request(self, *args, **kwargs):
        """
        Runs validation and the process method
        :param args:
        :param kwargs:
        :return:
        """

        method = self.request.method.lower()

        if not getattr(self, method):
            raise UnsupportedResourceMethodException

        self.validate_request(*args, **kwargs)

        # call appropriate resource method
        getattr(self, method)(*args, **kwargs)

    # handle all requests by the one way
    on_get = on_post = on_head = on_put = on_patch = on_delete = handle_request

    def prepare_request(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        self.params = {}

        if self.request.content_length in (None, 0):
            return

        body = self.request.stream.read()
        if not body:
            return

        try:
            self.params = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            return

    def prepare_response(self, *args, **kwargs):
        """
        Prepares response
        :param args:
        :param kwargs:
        :return:
        """
        exception = self.raised_exception if hasattr(self, 'raised_exception') else None
        if exception:
            self.response.body = exception.message
            self.response.status = exception.status_code
            return

        # if you want to do response with some data instead of string just set self.response_data field
        response_data = self.response_data if hasattr(self, 'response_data') else None
        if response_data:
            self.response.body = json.dumps(self.response_data)
            return

    def validate_request(self, *args, **kwargs):
        """
        Checks request data before process
        :param req:
        :param args:
        :param kwargs:
        :return:
        """
        if self.data_schema:
            params = self.params
            schema_validator = Schema(self.data_schema)

            try:
                params = schema_validator(params)
            except MultipleInvalid as e:
                error = e.errors[0]
                parameter_name = error.path[0]

                if isinstance(error, RequiredFieldInvalid):
                    raise MissingParameterException(parameter_name)
                else:
                    raise InvalidParameterFormatException(parameter_name, error.message)

            # Rewrite the data because it may be changed by schema validator (converted to appropriate type for example)
            self.params = params

        # Now we can validate high level conditions like entity existing or something else that is more complex than
        # format validation
        for validator in self.validators:
            validator(self, *args, **kwargs)



class ResourceSetupMiddleware(object):

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource):

        if not resource:
            return

        resource._cleanup()

        resource.request = req
        resource.response = resp

    def process_response(self, req, resp, resource):
        pass
