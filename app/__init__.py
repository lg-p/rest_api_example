import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import Config


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

    engine = create_engine('sqlite:///db.sqlite')
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    Base = declarative_base()
    Base.query = session.query_property()

    @_app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    return _app


if __name__ == "__main__":
    app = create_app()
    app.run()
