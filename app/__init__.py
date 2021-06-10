import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec
import logging

from config import Config

db = SQLAlchemy()
migrate = Migrate()
docs = FlaskApiSpec()


def create_app(test_config=None):
    _app = Flask(__name__)
    _app.config.from_mapping(
        SECRET_KEY="dev"
    )

    if test_config is None:
        _app.config.from_object(Config)
    else:
        _app.config.from_object(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(_app.instance_path)
    except OSError:
        pass

    db.init_app(_app)
    migrate.init_app(_app, db)

    from app.registration import bp_reg
    _app.register_blueprint(bp_reg, url_prefix='/api')

    from app.authentication import bp_auth
    _app.register_blueprint(bp_auth, url_prefix='/api')

    from app.items import bp_it
    _app.register_blueprint(bp_it, url_prefix='/api')

    jwt = JWTManager(_app)
    jwt.init_app(_app)

    docs.init_app(_app)

    return _app


def setup_logger():
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)

    if not os.path.exists(Config.LOG_URL):
        os.makedirs(Config.LOG_URL)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler(os.path.join(Config.LOG_URL, 'api.log'))
    file_handler.setFormatter(formatter)

    _logger.addHandler(file_handler)

    return _logger


logger = setup_logger()

my_app = create_app()
client = my_app.test_client()
with my_app.app_context():
    db.create_all()


if __name__ == "__main__":
    my_app.run()


from app.registration.view import *
from app.authentication.view import *
from app.items.view import *
