from annoying import __version__

from setuptools import setup, find_packages
setup(
    name="django-annoying",
    version=__version__,
    packages=find_packages(),
    author="Stavros Korokithakis",
    author_email="stavros@korokithakis.net",
    description="This is a django application that tries to eliminate annoying things in the Django framework.",
    long_description="""
        **Features:**

            - render_to decorator - Reduce typing in django views.
            - signals decorator - Allow using signals as decorators.
            - ajax_request decorator - Returns JsonResponse with dict as content.
            - autostrip decorator - Strip form text fields before validation.
            - get_object_or_None function - Similar to get_object_or_404, but returns None if the object is not found.
            - get_config function - Get settings from django.conf if exists, return a default value otherwise.
            - AutoOneToOne field - Creates related object on first call if it doesn't exist yet.
            - HttpResponseReload - Reload and stay on same page from where request was made.
            - StaticServer middleware - Instead of configuring urls.py, just add this middleware and it will serve you static files.
            - JSONField - A field that stores a Python object as JSON and retrieves it as a Python object.


        **Installation instructions:**

             - Copy the "annoying" directory to your Django project or put it in your PYTHONPATH.
             - You can also run "python setup.py install", "easy_install django-annoying", or "pip install django-annoying".


        **Download:**

            - git clone git://github.com/skorokithakis/django-annoying.git
            - hg clone http://bitbucket.org/Stavros/django-annoying/

    """,
    license="BSD",
    keywords="django",
    url="https://github.com/skorokithakis/django-annoying",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
