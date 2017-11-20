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

    extensions(app)

    with app.app_context():
        from app.models import User, MqttClient, MqttAccess
        db.create_all()

        admin = User.query.filter_by(is_admin=True).first()

        if not admin:
            admin = User()
            admin.username = 'averdier'
            admin.hash_password('averdier')
            admin.is_admin = True

            db.session.add(admin)
            db.session.commit()

    return app


def extensions(app):
    """
    Init extensions

    :param app: Flask app
    """
    db.init_app(app)