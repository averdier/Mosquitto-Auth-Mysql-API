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


from .endpoints.token import ns as token_namespace
from .endpoints.clients import ns as client_namespace
from .endpoints.accesses import ns as accesses_namespace

api.add_namespace(token_namespace)
api.add_namespace(client_namespace)
api.add_namespace(accesses_namespace)