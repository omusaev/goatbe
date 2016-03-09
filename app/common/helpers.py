# -*- coding: utf-8 -*-

from importlib import import_module

import settings as app_settings


__all__ = (
    'import_by_path',
    'collect_installed_resources',
)


def import_by_path(dotted_path, error_prefix=''):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. RaiseImproperlyConfigured if something goes wrong.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise Exception("%s%s doesn't look like a module path" % (error_prefix, dotted_path))
    try:
        module = import_module(module_path)
    except ImportError as e:
        raise Exception('%sError importing module %s: "%s"' % (error_prefix, module_path, e))

    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise Exception('%sModule "%s" does not define a "%s" attribute/class' % (
            error_prefix, module_path, class_name))
    return attr


def collect_installed_resources():
    for resource_path in app_settings.INSTALLED_RESOURCES:
        resource = import_by_path(resource_path)
        resource_obj = resource()

        yield resource_obj
