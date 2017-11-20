# -*- coding: utf-8 -*-

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration
    """
    SECRET_KEY = os.environ.get('MOSQUITTO_AUTH_KEY') or 'djkugjycvdfdfgd!'
    TOKEN_EXPIRATION_TIME = 600
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True

    @staticmethod
    def init_app(app):
        """
        Init app

        :param app: Flask App
        :type app: Flask
        """
        pass


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@localhost/mosquitto_auth?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = True


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@localhost/mosquitto_auth?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTPLUS_MASK_SWAGGER = True
    RESTPLUS_ERROR_404_HELP = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}