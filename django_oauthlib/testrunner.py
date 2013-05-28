import sys
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='django_oauthlib.urls',
    INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', 'django_oauthlib',)
)


def run_tests():
    import django.test.utils
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['django_oauthlib'])
    sys.exit(failures)
