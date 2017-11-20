# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restplus import Api


authorizations = {
    'tokenKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'basicAuth': {
        'type': 'basic',
        'in': 'header'
    }
}

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='Mosquitto Auth Mysql API',
          version='0.1',
          description='Mosquitto Auth Mysql API',
          authorizations=authorizations,
          security='tokenKey'
          )