from setuptools import setup, find_packages
setup(
    name = "django-annoying",
    version = "0.7.6",
    packages = find_packages(),
    author = "Anderson",
    author_email = "self.anderson@gmail.com",
    description = "This is a django application that tries to eliminate annoying things in the Django framework.",
    long_description = """
        **Features:**

            - render_to decorator - reduce typing in django views.
            - signals decorator - allow use signals as decorators.
            - ajax_request decorator - returns JsonResponse with this dict as content.
            - autostrip decorator - strip text form fields before validation.
            - get_object_or_None function - similar to get_object_or_404, but returns None if object not found.
            - get_config function - get settings from django.conf if exists, return default value otherwise.
            - AutoOneToOne field - creates related object on first call if it doesnt exist yet.
            - HttpResponseReload - reload and stay on same page from where request was made.
            - StaticServer middleware - instead of configuring urls.py, just add this middleware and it will serve you static files.
            - JSONField - custom field that lets you easily store JSON data in one of your model fields.

                     

        **Installation instruction:**

             - Copy annoying directory to your django project or put in PYTHONPATH
             - Also you can run sudo python setup.py install or sudo easy_install django-annoying

                              

        **Download:**

            - hg clone http://bitbucket.org/offline/django-annoying/

    """,
    license = "BSD",
    keywords = "django",
    url = "http://bitbucket.org/offline/django-annoying/wiki/Home",
)
