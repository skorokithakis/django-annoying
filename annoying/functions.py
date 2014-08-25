from django.shortcuts import _get_queryset
from django.conf import settings


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_config(key, default=None):
    """
    Get settings from django.conf if exists,
    return default value otherwise

    example:

    ADMIN_EMAIL = get_config('ADMIN_EMAIL', 'default@email.com')
    """
    return getattr(settings, key, default)


def get_object_or_this(model, this=None, *args, **kwargs):
    """
    Uses get() to return an object or the value of <this> argument
    if object does not exist.

    If the <this> argument if not provided None would be returned.
    <model> can be either a QuerySet instance or a class.
    """

    return get_object_or_None(model, *args, **kwargs) or this
