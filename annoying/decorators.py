from django.shortcuts import render_to_response
from django import forms
from django import VERSION as DJANGO_VERSION
from django.template import RequestContext
from django.db.models import signals as signalmodule
from django.http import HttpResponse
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

# Try to be compatible with Django 1.5+.
try:
    import json
except ImportError:
    from django.utils import simplejson as json

# Basestring no longer exists in Python 3
try:
    basestring
except:
    basestring = str

import datetime
import os

__all__ = ['render_to', 'signals', 'ajax_request', 'autostrip']


try:
    from functools import wraps
except ImportError:
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),
              updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner


def render_to(template=None, content_type=None, mimetype=None):
    """
    Decorator for Django views that sends returned dict to render_to_response
    function.

    Template name can be decorator parameter or TEMPLATE item in returned
    dictionary.  RequestContext always added as context instance.
    If view doesn't return dict then decorator simply returns output.

    Parameters:
     - template: template name to use
     - content_type: content type to send in response headers
     - mimetype: content type to send in response headers (deprecated)

    Examples:
    # 1. Template name in decorator parameters

    @render_to('template.html')
    def foo(request):
        bar = Bar.object.all()
        return {'bar': bar}

    # equals to
    def foo(request):
        bar = Bar.object.all()
        return render_to_response('template.html',
                                  {'bar': bar},
                                  context_instance=RequestContext(request))


    # 2. Template name as TEMPLATE item value in return dictionary.
         if TEMPLATE is given then its value will have higher priority
         than render_to argument.

    @render_to()
    def foo(request, category):
        template_name = '%s.html' % category
        return {'bar': bar, 'TEMPLATE': template_name}

    #equals to
    def foo(request, category):
        template_name = '%s.html' % category
        return render_to_response(template_name,
                                  {'bar': bar},
                                  context_instance=RequestContext(request))

    """
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            if tmpl is None:
                template_dir = os.path.join(*function.__module__.split('.')[:-1])
                tmpl = os.path.join(template_dir, function.func_name + ".html")
            # Explicit version check to avoid swallowing other exceptions
            if DJANGO_VERSION[0] >= 1 and DJANGO_VERSION[1] >= 5:
                return render_to_response(tmpl, output, \
                        context_instance=RequestContext(request),
                        content_type=content_type or mimetype)
            else:
                return render_to_response(tmpl, output, \
                        context_instance=RequestContext(request),
                        mimetype=content_type or mimetype)
        return wrapper
    return renderer


class Signals(object):
    '''
    Convenient wrapper for working with Django's signals (or any other
    implementation using same API).

    Example of usage::


       # connect to registered signal
       @signals.post_save(sender=YourModel)
       def sighandler(instance, **kwargs):
           pass

       # connect to any signal
       signals.register_signal(siginstance, signame) # and then as in example above

       or

       @signals(siginstance, sender=YourModel)
       def sighandler(instance, **kwargs):
           pass

    In any case defined function will remain as is, without any changes.

    (c) 2008 Alexander Solovyov, new BSD License
    '''
    def __init__(self):
        self._signals = {}

        # register all Django's default signals
        for k, v in signalmodule.__dict__.items():
            # that's hardcode, but IMHO it's better than isinstance
            if not k.startswith('__') and k != 'Signal':
                self.register_signal(v, k)

    def __getattr__(self, name):
        return self._connect(self._signals[name])

    def __call__(self, signal, **kwargs):
        def inner(func):
            signal.connect(func, **kwargs)
            return func
        return inner

    def _connect(self, signal):
        def wrapper(**kwargs):
            return self(signal, **kwargs)
        return wrapper

    def register_signal(self, signal, name):
        self._signals[name] = signal

signals = Signals()


FORMAT_TYPES = {
    'application/json': lambda response: json.dumps(response, cls=DjangoJSONEncoder),
    'text/json':        lambda response: json.dumps(response, cls=DjangoJSONEncoder),
}

try:
    import yaml
except ImportError:
    pass
else:
    FORMAT_TYPES.update({
        'application/yaml': yaml.dump,
        'text/yaml':        yaml.dump,
    })


def ajax_request(func):
    """
    If view returned serializable dict, returns response in a format requested
    by HTTP_ACCEPT header. Defaults to JSON if none requested or match.

    Currently supports JSON or YAML (if installed), but can easily be extended.

    example:

        @ajax_request
        def my_view(request):
            news = News.objects.all()
            news_titles = [entry.title for entry in news]
            return {'news_titles': news_titles}
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        for accepted_type in request.META.get('HTTP_ACCEPT', '').split(','):
            if accepted_type in FORMAT_TYPES.keys():
                format_type = accepted_type
                break
        else:
            format_type = 'application/json'
        response = func(request, *args, **kwargs)
        if not isinstance(response, HttpResponse):
            if hasattr(settings, 'FORMAT_TYPES'):
                format_type_handler = settings.FORMAT_TYPES[format_type]
                if hasattr(format_type_handler, '__call__'):
                    data = format_type_handler(response)
                elif isinstance(format_type_handler, basestring):
                    mod_name, func_name = format_type_handler.rsplit('.', 1)
                    module = __import__(mod_name, fromlist=[func_name])
                    function = getattr(module, func_name)
                    data = function(response)
            else:
                data = FORMAT_TYPES[format_type](response)
            response = HttpResponse(data, content_type=format_type)
            response['content-length'] = len(data)
        return response
    return wrapper


def autostrip(cls):
    """
    strip text fields before validation

    example:
    class PersonForm(forms.Form):
        name = forms.CharField(min_length=2, max_length=10)
        email = forms.EmailField()

    PersonForm = autostrip(PersonForm)

    #or you can use @autostrip in python >= 2.6

    Author: nail.xx
    """
    fields = [(key, value) for key, value in cls.base_fields.iteritems() if isinstance(value, forms.CharField)]
    for field_name, field_object in fields:
        def get_clean_func(original_clean):
            return lambda value: original_clean(value and value.strip())
        clean_func = get_clean_func(getattr(field_object, 'clean'))
        setattr(field_object, 'clean', clean_func)
    return cls
