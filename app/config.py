from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


class Config:
    SECRET_KEY = "563769c265a946ca9edd9ef023d8f741"
    APISPEC_SPEC = APISpec(
        title='API Users',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    )
    APISPEC_SWAGGER_URL = '/swagger'
