from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import AuthorizationView, TokenView, ErrorView

urlpatterns = patterns('',
    url(r'^oauth/2/authorize/$', login_required(AuthorizationView.as_view()), name='oauth2_authorize'),
    url(r'^oauth/2/token/$', TokenView.as_view(), name='oauth2_token'),
    url(r'^oauth/2/error/$', ErrorView.as_view(), name='oauth2_error'),
)
