from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import signals as signalmodule


def render_to(template=None):
    """
    Decorator for Django views that sends returned dict to render_to_response function.

    Template name can be decorator parameter or TEMPLATE item in returned dictionary.
    RequestContext always added as context instance.
    If view doesn't return dict then decorator simply returns output.

    Parameters:
     - template: template name to use

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


    # 2. Template name as TEMPLATE item value in return dictionary

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
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            return render_to_response(tmpl, output, context_instance=RequestContext(request))
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
        for k, v in signalmodule.__dict__.iteritems():
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
