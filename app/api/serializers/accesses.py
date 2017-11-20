# -*- coding: utf-8 -*-

from flask_restplus import fields
from . import api


access_post = api.model('Access post', {
    'topic': fields.String(required=True, min_length=3, max_length=256, description='Mqtt topic'),
    'username': fields.String(required=True, min_length=3, max_length=32, desciption='Client username'),
    'access': fields.Integer(required=True, min=1, max=2, default=1,
                             description='Access type (1 for read only, 2 for read and write')
})

access_patch = api.model('Access patch', {
    'topic': fields.String(required=False, min_length=3, max_length=256, description='Mqtt totpic'),
    'access': fields.Integer(required=False, min=1, max=2, default=1,
                             description='Access type (1 for read only, 2 for read and write')
})

access_minimal = api.model('Access minimal', {
    'id': fields.Integer(required=True, description='User unique id'),
    'topic': fields.String(required=True, description='Mqtt topic'),
    'username': fields.String(required=True, desciption='Client username'),
    'access': fields.Integer(required=True, description='Access type (1 for read only, 2 for read and write')
})

access_data_container = api.model('Access DataCOntainer', {
    'accesses': fields.List(fields.Nested(access_minimal), required=True, description='Access list')
})
