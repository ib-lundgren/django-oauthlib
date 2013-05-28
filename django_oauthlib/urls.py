from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import AuthorizationView, TokenView

urlpatterns = patterns('',
    url(r'^oauth/2/authorize/$', AuthorizationView.as_view(), name='oauth2_authorize'),
    url(r'^oauth/2/token/$', TokenView.as_view(), name='oauth2_token'),
)
