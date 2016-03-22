# -*- coding: utf-8 -*-

__all__ = (
    'BaseValidator',
)


class BaseValidator(object):

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, resource, *args, **kwargs):
        raise NotImplementedError
