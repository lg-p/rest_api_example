import os

from flask import Flask

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

    return _app


if __name__ == "__main__":
    app = create_app()
    app.run()
