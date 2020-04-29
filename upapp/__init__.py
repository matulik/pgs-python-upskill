import os
from flask import Flask

from .aws.aws import AWS
from .user.api import bp as user_bp
from upapp import db

db_file = ''


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.config['MAX_CONTENT_'] = '1000 * 1024'

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(user_bp)

    return app
