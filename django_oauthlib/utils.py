import logging
log = logging.getLogger('django-oauthlib')

from oauthlib.common import urlencode


def extract_params(request):
    log.debug('Extracting parameters from request.')
    uri = request.build_absolute_uri()
    http_method = request.method
    headers = request.META
    if 'wsgi.input' in headers:
        del headers['wsgi.input']
    if 'wsgi.errors' in headers:
        del headers['wsgi.errors']
    if 'HTTP_AUTHORIZATION' in headers:
        headers['Authorization'] = headers['HTTP_AUTHORIZATION']
    body = urlencode(request.POST.items())
    return uri, http_method, body, headers
