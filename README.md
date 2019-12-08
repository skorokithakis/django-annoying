Description
-----------

[![Code Shelter](https://www.codeshelter.co/static/badges/badge-flat.svg)](https://www.codeshelter.co/)

This django application eliminates certain annoyances in the Django
framework.

### Features

-   [render_to decorator](#render_to-decorator) - Reduce typing in django views.
-   [signals decorator](#signals-decorator) - Allow using signals as decorators.
-   [ajax_request decorator](#ajax_request-decorator) - Returns JsonResponse with dict as content.
-   [autostrip decorator](#autostrip-decorator) - Strip form text fields before validation
-   [get_object_or_None function](#get_object_or_none-function) - Similar to get_object_or_404, but returns None if the object is not found.
-   [AutoOneToOne field](#autoonetoonefield) - Creates a related object on first call if it doesn't exist yet.
-   [JSONField](#jsonfield) - A field that stores a Python object as JSON and retrieves it as a Python object.
-   [get_config function](#get_config-function) - Get settings from django.conf if exists, return a default value otherwise.
-   [StaticServer middleware](#staticserver-middleware) - Instead of configuring urls.py, just add
    this middleware and it will serve your static files when you are in
    debug mode.
-   [get_ object_or_this_function](#get_object_or_this-function) - Similar to get_object_or_404, but returns a default object (`this`) if the object is not found.
-   HttpResponseReload - Reload and stay on same page from where the request
    was made.

### Installation instructions

-   Copy the `annoying` directory to your django project or put in on your PYTHONPATH.
-   You can also run `python setup.py install`, `easy_install django-annoying`,
    or `pip install django-annoying`.
-   Add `"annoying"` under INSTALLED\_APPS in your `settings.py` file.
-   Django-annoying requires Django 1.11 or later.

Examples
--------

### render_to decorator

```python
from annoying.decorators import render_to

# 1. Template name in decorator parameters

@render_to('template.html')
def foo(request):
    bar = Bar.object.all()
    return {'bar': bar}

# equals to
def foo(request):
    bar = Bar.object.all()
    return render(request, 'template.html', {'bar': bar})


# 2. Template name as TEMPLATE item value in return dictionary

@render_to()
def foo(request, category):
    template_name = '%s.html' % category
    return {'bar': bar, 'TEMPLATE': template_name}

#equals to
def foo(request, category):
    template_name = '%s.html' % category
    return render(request, template_name, {'bar': bar})
```

### signals decorator

Note: `signals` is deprecated and will be removed in a future version. Django now [includes this by default](https://docs.djangoproject.com/en/stable/topics/signals/#connecting-receiver-functions).

```python
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
```

### ajax_request decorator

The `ajax_request` decorator converts a `dict` or `list` returned by a view to a JSON or YAML object,
depending on the HTTP `Accept` header (defaults to JSON, requires `PyYAML` if you want to accept YAML).

```python
from annoying.decorators import ajax_request

@ajax_request
def my_view(request):
    news = News.objects.all()
    news_titles = [entry.title for entry in news]
    return {'news_titles': news_titles}
```

### autostrip decorator

Note: `autostrip` is deprecated and will be removed in a future version. Django now [includes this by default](https://docs.djangoproject.com/en/stable/ref/forms/fields/#django.forms.CharField.strip).

```python
from annoying.decorators import autostrip

@autostrip
class PersonForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=10)
    email = forms.EmailField()
```

### get_object_or_None function

```python
from annoying.functions import get_object_or_None

def get_user(request, user_id):
    user = get_object_or_None(User, id=user_id)
    if not user:
        ...
```

### AutoOneToOneField

```python
from annoying.fields import AutoOneToOneField


class MyProfile(models.Model):
    user = AutoOneToOneField(User, primary_key=True)
    home_page = models.URLField(max_length=255, blank=True)
    icq = models.IntegerField(blank=True, null=True)
```

### JSONField

Note that if you're using Postgres you can use the built-in [django.contrib.postgres.fields.JSONField](https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/fields/#jsonfield), or if you're using
MySQL/MariaDB you can use [Django-MySQL's JSONField](https://django-mysql.readthedocs.io/en/latest/model_fields/json_field.html).

```python
from annoying.fields import JSONField


#model
class Page(models.Model):
    data = JSONField(blank=True, null=True)



# view or another place..
page = Page.objects.get(pk=5)
page.data = {'title': 'test', 'type': 3}
page.save()
```

### get_config function

```python
from annoying.functions import get_config

ADMIN_EMAIL = get_config('ADMIN_EMAIL', 'default@email.com')
```

### StaticServer middleware

Add this middleware as first item in MIDDLEWARE\_CLASSES(or MIDDLEWARE)

example:

```python
MIDDLEWARE_CLASSES = (  # MIDDLEWARE if you're using the new-style middleware
    'annoying.middlewares.StaticServe',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
```

It will serve static files in debug mode. Also it helps when you debug
one of your middleware by responding to static requests before they get
to debugged middleware and will save you from constantly typing "continue"
in debugger.


### get_object_or_this function

```python
from annoying.functions import get_object_or_this

def get_site(site_id):
    base_site = Site.objects.get(id=1)

    # Get site with site_id or return base site.
    site = get_object_or_this(Site, base_site, id=site_id)

    ...
    ...
    ...

    return site
```
