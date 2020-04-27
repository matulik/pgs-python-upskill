import os
from flask import Flask
from .user.api import bp as user_bp
from upapp import db

db_file = ''


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.db_session.remove()

    app.register_blueprint(user_bp)

    return app
