# -*- coding: utf-8 -*-

from flask import Flask
from app.extensions import db
from config import config


def create_app(config_name='default'):
    """
    Create Flask app

    :param config_name:
    :return: Flask
    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint)

    extensions(app)

    with app.app_context():
        from app.models import User, MqttClient, MqttAccess
        db.create_all()

        if len(User.query.all()) == 0:
            admin = User(username='averdier')
            admin.hash_password('by6WqIAxG3Ah')
            db.session.add(admin)
            db.session.commit()

    return app


def extensions(app):
    """
    Init extensions

    :param app: Flask app
    """
    db.init_app(app)