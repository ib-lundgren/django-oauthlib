from __future__ import absolute_import

from oauthlib.oauth2 import RequestValidator

from .models import Client
from .utils import log


class DjangoValidator(RequestValidator):

    # Ordered roughly in order of appearance in the authorization grant flow

    # Pre- and post-authorization.

    def validate_client_id(self, client_id, request, *args, **kwargs):
        try:
            request._client = Client.objects.get(client_id=client_id)
            return True
        except Client.DoesNotExist:
            return False

    def validate_redirect_uri(self, client_id, redirect_uri, request, *args, **kwargs):
        return redirect_uri in request._client.redirect_uris

    def get_default_redirect_uri(self, client_id, request, *args, **kwargs):
        # TODO: define default on model
        uris = request._client.redirect_uris.split(' ')
        return uris[0] if uris else None

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        if scopes is None:
            return False
        return all(map(lambda s: s in request._client.scopes, scopes))

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        # TODO: define default on model
        scopes = request._client.scopes.split(' ')
        return scopes[0] if scopes else None

    def validate_response_type(self, client_id, response_type, client, request, *args, **kwargs):
        return request._client.response_type == response_type

    # Post-authorization

    def save_authorization_code(self, client_id, code, request, *args, **kwargs):
        # Remember to associate it with request.scopes, request.redirect_uri
        # request.client, request.state and request.user (the last is passed in
        # post_authorization credentials, i.e. { 'user': request.user}.
        pass

    # Token request

    def authenticate_client(self, request, *args, **kwargs):
        # Whichever authentication method suits you, HTTP Basic might work
        pass

    def authenticate_client_id(self, client_id, request, *args, **kwargs):
        # Don't allow public (non-authenticated) clients
        return False

    def validate_code(self, client_id, code, client, request, *args, **kwargs):
        # Validate the code belongs to the client. Add associated scopes,
        # state and user to request.scopes, request.state and request.user.
        pass

    def confirm_redirect_uri(self, client_id, code, redirect_uri, client, *args, **kwargs):
        # You did save the redirect uri with the authorization code right?
        pass

    def validate_grant_type(self, client_id, grant_type, client, request, *args, **kwargs):
        # Clients should only be allowed to use one type of grant.
        # In this case, it must be "authorization_code" or "refresh_token"
        pass

    def save_bearer_token(self, token, request, *args, **kwargs):
        # Remember to associate it with request.scopes, request.user and
        # request.client. The two former will be set when you validate
        # the authorization code. Don't forget to save both the
        # access_token and the refresh_token and set expiration for the
        # access_token to now + expires_in seconds.
        pass

    def invalidate_authorization_code(self, client_id, code, request, *args, **kwargs):
        # Authorization codes are use once, invalidate it when a Bearer token
        # has been acquired.
        pass

    # Protected resource request

    def validate_bearer_token(self, token, scopes, request):
        # Remember to check expiration and scope membership
        pass

    # Token refresh request

    def confirm_scopes(self, refresh_token, scopes, request, *args, **kwargs):
        # If the client requests a set of scopes, assure that those are the
        # same as, or a subset of, the ones associated with the token earlier.
        pass
