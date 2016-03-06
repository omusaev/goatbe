# -*- coding: utf-8 -*-

import json

from voluptuous import (
    Schema, MultipleInvalid,
    RequiredFieldInvalid,
)

from common.exceptions import (
    GoatBaseException,
    UnsupportedResourceMethod,
    MissingParameterException,
    InvalidParameterFormatException,
)

__all__ = (
    'BaseResource',
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

    request = None
    response = None
    response_data = None
    raised_exception = None

    @property
    def url(self):
        return self.url

    def handle_request(self, req, resp, *args, **kwargs):
        """
        Common entry point. Prepares request, processes request and prepares response
        :param req:
        :param resp:
        :param args:
        :param kwargs:
        :return:
        """
        self.request = req
        self.response = resp

        try:
            self.prepare_request(*args, **kwargs)
            self.process_request(*args, **kwargs)
        except GoatBaseException as e:
            self.raised_exception = e

        self.prepare_response()
        self.clean()

    def clean(self):
        # we have to clean resource object fields because it may be used again without recreation
        self.request = self.response = self.response_data = self.raised_exception = None

    def process_request(self, *args, **kwargs):
        """
        Runs validation and the process method
        :param args:
        :param kwargs:
        :return:
        """

        method = self.request.method.lower()

        if not hasattr(self, method):
            raise UnsupportedResourceMethod

        self.validate_request(*args, **kwargs)

        # call appropriate resource method
        getattr(self, method)(*args, **kwargs)

    # handle all requests by the one way
    on_get = on_post = on_head = on_put = handle_request

    def prepare_request(self, *args, **kwargs):
        """
        Prepares request before process. For example, you can decode json-ed request.stream and set data to _params field
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def prepare_response(self, *args, **kwargs):
        """
        Prepares response
        :param args:
        :param kwargs:
        :return:
        """
        exception = self.raised_exception

        if exception:
            self.response.body = exception.message
            self.response.status = exception.status_code
            return

        # if you want to do response with some data instead of string just set self.response_data field
        if self.response_data:
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
            params = self.request.params
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
            self.request._params = params

        # Now we can validate high level conditions like entity existing or something else that is more complex than
        # format validation
        for validator in self.validators:
            validator(self.request, *args, **kwargs)
