import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec

from app.config import Config

engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

docs = FlaskApiSpec()


def create_app(test_config=None):
    _app = Flask(__name__)
    _app.config.from_mapping(
        SECRET_KEY="dev"
    )

    if test_config is None:
        _app.config.from_object(Config)
    else:
        _app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(_app.instance_path)
    except OSError:
        pass

    from app.registration import bp_reg
    _app.register_blueprint(bp_reg, url_prefix='/api')

    from app.authentication import bp_auth
    _app.register_blueprint(bp_auth, url_prefix='/api')

    from app.items import bp_it
    _app.register_blueprint(bp_it, url_prefix='/api')

    jwt = JWTManager(_app)

    docs.init_app(_app)

    return _app


if __name__ == "__main__":
    app = create_app()

    from models import *
    Base.metadata.create_all(bind=engine)

    app.run()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()
