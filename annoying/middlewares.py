import re

from django.conf import settings
from django.views.static import serve



class StaticServe(object):
    """
    Django middleware for serving static files instead of using urls.py
    
    """

    def process_request(self, request):
        if settings.DEBUG:
            regex = re.search(r'^%s(?P<path>.*)$' % settings.MEDIA_URL, request.path)
            if regex:
                return serve(request, regex.group(1), settings.MEDIA_ROOT)
