# -*- coding: utf-8 -*-

from voluptuous import Schema, ExactSequenceInvalid, Invalid

__all__ = (
    'ListOf',
)


class ListOf(object):

    def __init__(self, validator, **kwargs):
        self.msg = kwargs.pop('msg', None)
        self.schema = Schema(validator, **kwargs)

    def __call__(self, v):
        if not isinstance(v, (list, tuple)):
            raise ExactSequenceInvalid(self.msg)
        try:
            v = type(v)(self.schema(x) for x in v)
        except Invalid as e:
            raise e if self.msg is None else ExactSequenceInvalid(self.msg)
        return v
