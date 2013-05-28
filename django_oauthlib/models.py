from django.contrib.auth.models import User
from django.db import models
import json


class Client(models.Model):
    user = models.ForeignKey(User)
    response_type = models.CharField(max_length=20,
            choices=(
                ('code', 'Authorization code'),
                ('token', 'Implicit token'),
    ))
    grant_type = models.CharField(max_length=20, choices=(
        ('authorization_code', 'Authorization code'),
        ('password', 'Password credentials'),
        ('client_credentials', 'Client credentials'),
    ))
    client_id = models.TextField(unique=True)
    scopes = models.TextField()
    redirect_uris = models.TextField()

    def to_json(self):
        return json.dumps({
            'client_id': self.client_id,
        })


class BearerToken(models.Model):
    client = models.ForeignKey(Client, blank=True, null=True)
    user = models.ForeignKey(User)
    scopes = models.TextField()
    token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()


class AuthorizationCode(models.Model):
    client = models.ForeignKey(Client)
    scopes = models.TextField()
    state = models.TextField()
    code = models.TextField()
    redirect_uri = models.TextField()
    using_default_redirect_uri = models.BooleanField()
    user = models.ForeignKey(User)
