# -*- coding: utf-8 -*-

from voluptuous import *


# Refactor that
class ListOf(object):
    """Matches each element in a sequence against the corresponding element in
    the validators.

    :param msg: Message to deliver to user if validation fails.
    :param kwargs: All other keyword arguments are passed to the sub-Schema
        constructors.

    >>> from voluptuous import *
    >>> validate = Schema(ExactSequence([str, int, list, list]))
    >>> validate(['hourly_report', 10, [], []])
    ['hourly_report', 10, [], []]
    >>> validate(('hourly_report', 10, [], []))
    ('hourly_report', 10, [], [])
    """

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

    def __repr__(self):
        return 'ExactSequence([%s])' % (", ".join(repr(v)
                                                  for v in self.validators))
