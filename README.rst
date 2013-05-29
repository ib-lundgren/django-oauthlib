Django-OAuthLib
===============

** This project will be merged into `django-oauth-toolkit`_ **

Starting as a migration of the django decorator from `OAuthLib`_ this project
will aim to become a full featured, secure, easy to use OAuth provider
extension for Django supplying everything you will need to protect your
precious API with OAuth, both OAuth 1 and OAuth 2 will be supported.

Sounds like something you would like to help out with? Let me know by opening
an issue or getting in touch on `G+`_ or IRC (#oauthlib on Freenode).

.. _`django-oauth-toolkit`: https://github.com/evonove/django-oauth-toolkit
.. _`OAuthLib`: https://github.com/idan/oauthlib
.. _`G+`: https://plus.google.com/communities/101889017375384052571

Speculative usage
-----------------

Since Django provides both an ORM and a User model this extension should
be able to take care of almost all tasks related to OAuth without extra
configuration. 

The user will need to define scopes in settings...

.. code-block:: pycon

    from django.conf import settings
    settings.configure(OAUTH2_SCOPES = [
        'videos',
        'profile',
    ])

... and which views should be protected

.. code-block:: pycon

    from django_oauthlib import oauth2_provider

    @oauth2_provider.protected_resource_view(scopes=['profile'])
    def your_profile_view(request):
        ...

... and if they wish to customize the authorization view, they can by
changing the definition of ``actual_authorization_view`` in ``urls.py``.
