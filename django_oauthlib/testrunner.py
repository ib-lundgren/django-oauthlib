import logging
import sys
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='django_oauthlib.urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django_oauthlib',
    )
)


def run_tests():
    for log_id in ('oauthlib', 'django-oauthlib'):
        log = logging.getLogger(log_id)
        log.addHandler(logging.StreamHandler(sys.stdout))
        log.setLevel(logging.DEBUG)

    import django.test.utils
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['django_oauthlib'])
    sys.exit(failures)
