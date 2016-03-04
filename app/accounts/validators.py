# -*- coding: utf-8 -*-

from voluptuous import Invalid

from models import User, Card, CardTransaction, DBSession


__all__ = (
    'BaseValidator',
)


class BaseValidator():

    message = 'Error'

    def __init__(self, message=None):
        if message:
            self.message = message

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)

    def run(self, value):
        raise NotImplementedError
