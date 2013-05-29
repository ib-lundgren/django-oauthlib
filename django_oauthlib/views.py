from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

# TODO: don't import errors like this
from oauthlib.oauth2.draft25 import errors
from oauthlib.oauth2 import Server

from .validator import DjangoValidator
from .utils import extract_params, log


def get_credentials(request):
    return {}


def get_authorization(request):
    return request.POST.getlist(['scopes']), {'user': request.user}


def get_actual_authorization_view(request):
    # TODO: use template?
    def basic_view(request, client_id=None, scopes=None, **kwargs):
        response = HttpResponse()
        response.write('<h1> Authorize access to %s </h1>' % client_id)
        response.write('<form method="POST" action="/post_authorization">')
        for scope in scopes or []:
            response.write('<input type="checkbox" name="scopes" value="%s"/> %s' % (scope, scope))
        response.write('<input type="submit" value="Authorize"/>')
        return response
    return basic_view


class AuthorizationView(View):

    def __init__(self):
        validator = DjangoValidator()
        # TODO: this should probably be tunable through settings
        self._authorization_endpoint = Server(validator)
        self._error_uri = reverse('oauth2_error')

    def get(self, request, *args, **kwargs):
        uri, http_method, body, headers = extract_params(request)
        redirect_uri = request.GET.get('redirect_uri', None)
        log.debug('Found redirect uri %s.', redirect_uri)
        try:
            scopes, credentials = self._authorization_endpoint.validate_authorization_request(
                    uri, http_method, body, headers)
            log.debug('Saving credentials to session, %r.', credentials)
            request.session['oauth2_credentials'] = credentials
            kwargs['scopes'] = scopes
            kwargs.update(credentials)
            actual_view = get_actual_authorization_view(request)
            log.debug('Invoking actual view method, %r.', actual_view)
            return actual_view(request, *args, **kwargs)

        except errors.FatalClientError as e:
            log.debug('Fatal client error, redirecting to error page.')
            return HttpResponseRedirect(e.in_uri(self._error_uri))

        except errors.OAuth2Error as e:
            log.debug('Client error, redirecting back to client.')
            # TODO: remove after federico PR
            e.redirect_uri = redirect_uri or 'https://localhost'
            return HttpResponseRedirect(e.in_uri(e.redirect_uri))

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        uri, http_method, body, headers = extract_params(request)
        scopes, credentials = get_authorization(request)
        log.debug('Fetched credentials view, %r.', credentials)
        credentials.update(request.session.get('oauth2_credentials', {}))
        log.debug('Fetched credentials from session, %r.', credentials)
        redirect_uri = credentials.get('redirect_uri')
        log.debug('Found redirect uri %s.', redirect_uri)
        try:
            url, headers, body, status = self._authorization_endpoint.create_authorization_response(
                    uri, http_method, body, headers, scopes, credentials)
            log.debug('Authorization successful, redirecting to client.')
            return HttpResponseRedirect(url)
        except errors.FatalClientError as e:
            log.debug('Fatal client error, redirecting to error page.')
            return HttpResponseRedirect(e.in_uri(self._error_uri))
        except errors.OAuth2Error as e:
            log.debug('Client error, redirecting back to client.')
            return HttpResponseRedirect(e.in_uri(redirect_uri))


class TokenView(View):

    def __init__(self, token_endpoint):
        self._token_endpoint = token_endpoint

    def post(self, request, *args, **kwargs):
        uri, http_method, body, headers = extract_params(request)
        credentials = get_credentials(request)
        log.debug('Fetched credentials view, %r.', credentials)
        url, headers, body, status = self._token_endpoint.create_token_response(
                uri, http_method, body, headers, credentials)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response


class ErrorView(View):
    pass
