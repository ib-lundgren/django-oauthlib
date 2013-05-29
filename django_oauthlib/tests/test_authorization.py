from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from oauthlib.common import add_params_to_uri

from django_oauthlib.models import Client as _Client


class AuthorizationViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='test')
        self.web_client = _Client.objects.create(
                user=user,
                response_type='code',
                grant_type='authorization_code',
                client_id='foo',
                scopes='movies profile docs',
                redirect_uris='https://localhost/cb'
        )
        self.mobile_client = _Client.objects.create(
                user=user,
                response_type='token',
                client_id='bar',
                scopes='pictures profile docs',
                redirect_uris='https://localhost/callback'
        )
        self.auth = reverse('oauth2_authorize')
        self.error = reverse('oauth2_error')

    def test_pre_auth_valid(self):
        """Ensure auth code and implicit grant can authorize.

        Will test both provided and default redirect uris and scopes.
        """
        valid_params = ({
            'client_id': 'bar',
            'response_type': 'token',
        }, {
            'client_id': 'bar',
            'response_type': 'token',
            'redirect_uri': 'https://localhost/callback',
        }, {
            'client_id': 'bar',
            'response_type': 'token',
            'redirect_uri': 'https://localhost/callback',
            'scope': 'profile pictures',
        }, {
            'client_id': 'bar',
            'response_type': 'token',
            'scope': 'profile pictures',
        }, {
            'client_id': 'foo',
            'response_type': 'code',
        }, {
            'client_id': 'foo',
            'response_type': 'code',
            'redirect_uri': 'https://localhost/cb',
        }, {
            'client_id': 'foo',
            'response_type': 'code',
            'redirect_uri': 'https://localhost/cb',
            'scope': 'profile movies',
        }, {
            'client_id': 'foo',
            'response_type': 'code',
            'scope': 'profile movies',
        })
        for params in valid_params:
            c = Client()
            r = c.get(add_params_to_uri(self.auth, params.items()), follow=True)
            self.assertEqual(r.redirect_chain, [])
            self.assertEqual(r.status_code, 200)

    def test_pre_auth_fatal(self):
        """Invalid redirect uri or client id."""
        fatal_params = ({
            'response_type': 'token',
        }, {
            'client_id': 'invalid',
            'response_type': 'token',
        }, {
            'client_id': 'bar',
            'response_type': 'token',
            'redirect_uri': 'https://localhost/invalid',
        }, {
            'client_id': 'bar',
            'response_type': 'token',
            'redirect_uri': 'https://localhost/invalid',
            'scope': 'profile pictures',
        }, {
            'client_id': 'invalid',
            'response_type': 'code',
        }, {
            'client_id': 'foo',
            'response_type': 'code',
            'redirect_uri': 'https://localhost/invalid',
        }, {
            'client_id': 'foo',
            'response_type': 'code',
            'redirect_uri': 'https://localhost/invalid',
            'scope': 'profile movies',
        })
        for params in fatal_params:
            c = Client()
            r = c.get(add_params_to_uri(self.auth, params.items()), follow=True)
            self.assertIn(self.error, r.redirect_chain.pop()[0])
            # TODO: why is this 405 here?
            self.assertEqual(r.status_code, 405)

    def test_pre_auth_error(self):
        """Invalid requests parameters, unauthorized use etc."""
        invalid_params = ({
            'client_id': 'foo',
            'response_type': 'token',
        }, {
            'client_id': 'bar',
            'response_type': 'token',
            'redirect_uri': 'https://localhost/callback',
            'scope': 'profile invalid',
        }, {
            'client_id': 'bar',
            'response_type': 'token',
            'scope': 'profile invalid',
        }, {
            'client_id': 'bar',
            'response_type': 'code',
        }, {
            'client_id': 'foo',
            'response_type': 'code',
            'redirect_uri': 'https://localhost/cb',
            'scope': 'profile invalid',
        }, {
            'client_id': 'foo',
            'response_type': 'code',
            'scope': 'invalid movies',
        })
        for params in invalid_params:
            c = Client()
            r = c.get(add_params_to_uri(self.auth, params.items()), follow=True)
            self.assertIn(params.get('redirect_uri', 'https://localhost'),
                          r.redirect_chain.pop()[0])
            # TODO: why is this 404 here?
            self.assertEqual(r.status_code, 404)
