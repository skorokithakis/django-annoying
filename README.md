Description
-----------

This django application eliminates certain annoyances in the Django
framework.

### Features

-   render\_to decorator - reduce typing in django views.
-   signals decorator - allow use signals as decorators.
-   ajax\_request decorator - returns JsonResponse with dict as content.
-   autostrip decorator - strip form text fields before validation
-   get\_object\_or\_None function - similar to get\_object\_or\_404,
    but returns None if object not found.
-   get\_config function - get settings from django.conf if exists,
    return default value otherwise.
-   AutoOneToOne field - creates related object on first call if it
    doesnt exists yet.
-   JSONField - Field that store python object as json and retrieves it
    back as python object.
-   HttpResponseReload - reload and stay on same page from where request
    was made.
-   StaticServer middleware - instead of configuring urls.py, just add
    this middleware and it will serve your static files when you in
    debug mode

### Installation instruction

-   Copy annoying directory to your django project or put in on
    PYTHONPATH
-   Also you can run sudo python setup.py install, sudo easy\_install
    django-annoying, or sudo pip install django-annoying
-   Add "annoying" under INSTALLED\_APPS in your settings.py file

Examples
--------

### render\_to decorator

    from annoying.decorators import render_to

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

### signals decorator

    from annoying.decorators import signals

    # connect to registered signal
    @signals.post_save(sender=YourModel)
    def sighandler(instance, **kwargs):
        pass

    # connect to any signal
    signals.register_signal(siginstance, signame) # and then as in example above

    #or

    @signals(siginstance, sender=YourModel)
    def sighandler(instance, **kwargs):
        pass

    #In any case defined function will remain as is, without any changes.

### ajax\_request decorator

    from annoying.decorators import ajax_request

    @ajax_request
    def my_view(request):
        news = News.objects.all()
        news_titles = [entry.title for entry in news]
        return {'news_titles': news_titles}

### autostrip decorator

    from annoying.decorators import autostrip

    class PersonForm(forms.Form):
        name = forms.CharField(min_length=2, max_length=10)
        email = forms.EmailField()

    PersonForm = autostrip(PersonForm)

    #or in python >= 2.6

    @autostrip
    class PersonForm(forms.Form):
        name = forms.CharField(min_length=2, max_length=10)
        email = forms.EmailField()

### get\_object\_or\_None function

    from annoying.functions import get_object_or_None

    def get_user(request, user_id):
        user = get_object_or_None(User, id=user_id)
        if not user:
            ...

### AutoOneToOneField

    from annoying.fields import AutoOneToOneField


    class MyProfile(models.Model):
        user = AutoOneToOneField(User, primary_key=True)
        home_page = models.URLField(max_length=255, blank=True)
        icq = models.IntegerField(blank=True, null=True)

### JSONField

    from annoying.fields import JSONField


    #model
    class Page(models.Model):
        data = JSONField(blank=True, null=True)



    # view or another place..
    page = Page.objects.get(pk=5)
    page.data = {'title': 'test', 'type': 3}
    page.save()

### get\_config function

    from annoying.functions import get_config

    ADMIN_EMAIL = get_config('ADMIN_EMAIL', 'default@email.com')

### StaticServer middleware

Add this middleware as first item in MIDDLEWARE\_CLASSES

example:

    MIDDLEWARE_CLASSES = (
        'annoying.middlewares.StaticServe',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.doc.XViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    )

It will serve static files in debug mode. Also it helps when you debug
one of you middlewares by responding to static requests before they get
to debuged middleware and will save you from typing 100 times "continue"
in debuger.

Used on [python](http://pyplanet.org) community portal.
