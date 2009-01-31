from django.http import HttpResponse
from django.utils.encoding import iri_to_uri


class HttpResponseReload(HttpResponse):
    status_code = 302

    def __init__(self, request):
        HttpResponse.__init__(self)
        referer = request.META.get('HTTP_REFERER')
        self['Location'] = iri_to_uri(referer or "/")
