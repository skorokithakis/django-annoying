import re

from django.conf import settings
from django.views.static import serve



class StaticServe(object):
    """
    Django middleware for serving static files instead of using urls.py
    """
    regex = re.compile(r'^%s(?P<path>.*)$' % settings.MEDIA_URL)

    def process_request(self, request):
        if settings.DEBUG:
            match = self.regex.search(request.path)
            if match:
                return serve(request, match.group(1), settings.MEDIA_ROOT)
