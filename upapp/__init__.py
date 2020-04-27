import os
from flask import Flask

db_file = ''


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, db_file)
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import user

    app.register_blueprint(user.bp)

    return app
