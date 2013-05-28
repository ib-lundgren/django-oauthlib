from __future__ import absolute_import
import functools

from django.http import HttpResponseForbidden

from .utils import extract_params, log


class OAuth2ProviderDecorator(object):

    def __init__(self, resource_endpoint):
        self._resource_endpoint = resource_endpoint

    def protected_resource_view(self, scopes=None):
        def decorator(f):
            @functools.wraps(f)
            def wrapper(request, *args, **kwargs):
                try:
                    scopes_list = scopes(request)
                except TypeError:
                    scopes_list = scopes
                uri, http_method, body, headers = extract_params(request)
                log.debug('Authorizing request to %s.', uri)
                valid, r = self._resource_endpoint.verify_request(
                        uri, http_method, body, headers, scopes_list)
                # TODO: add to request object instead
                kwargs.update({
                    'client': r.client,
                    'user': r.user,
                    'scopes': r.scopes
                })
                if valid:
                    return f(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            return wrapper
        return decorator
