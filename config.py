import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "563769c265a946ca9edd9ef023d8f741"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_URL = os.path.join(basedir, 'log')
    APISPEC_SPEC = APISpec(
        title='API Users',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    )
    APISPEC_SWAGGER_URL = '/swagger'


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_URL = os.path.join(basedir, 'log')
