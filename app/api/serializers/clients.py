# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


client_post = api.model('Client post', {
    'username': fields.String(required=True, min_length=3, max_length=32, description='Client username'),
    'password': fields.String(required=True, min_length=3, max_length=16, description='Client password'),
    'is_admin': fields.Boolean(required=True, default=False, description='Client administrator status')
})

client_patch = api.model('Client patch', {
    'password': fields.String(required=False, min_length=3, max_length=16, description='Client password'),
    'is_admin': fields.Boolean(required=False, default=False, description='Client administrator status')
})

client_minimal = api.model('Client minimal', {
    'id': fields.Integer(required=True, description='Client unique ID'),
    'username': fields.String(required=True, description='Client username'),
    'is_admin': fields.Boolean(required=True, description='Client administrator status')
})

access_nested = api.model('Access nested', {
    'id': fields.Integer(required=True, description='User unique id'),
    'topic': fields.String(required=True, description='Mqtt topic'),
    'access': fields.Integer(required=True, description='Access type (1 for read only, 2 for read and write')
})

client_detail = api.inherit('Client detail', client_minimal, {
    'accesses': fields.List(fields.Nested(access_nested), required=True, description='Client accesses')
})

client_data_container = api.model('Client DataContainer', {
    'clients': fields.List(fields.Nested(client_minimal), required=True, description='Client list')
})