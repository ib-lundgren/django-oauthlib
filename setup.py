from os.path import dirname, join
from setuptools import setup, find_packages


def fread(fn):
    with open(join(dirname(__file__), fn), 'r') as f:
        return f.read()


requires = ['oauthlib']
tests_require = []

setup(
    name='django-oauthlib',
    version='0.0.1',
    description='Full featured OAuth provider extension for Django',
    long_description=fread('README.rst'),
    author='Ib Lundgren',
    author_email='ib.lundgren@gmail.com',
    url='https://github.com/ib-lundgren/django-oauthlib',
    license='BSD',
    packages=find_packages(exclude=('docs', 'tests', 'tests.*')),
    test_suite='django_oauthlib.testrunner.run_tests',
    tests_require=tests_require,
    extras_require={'test': tests_require},
    install_requires=requires,
)
