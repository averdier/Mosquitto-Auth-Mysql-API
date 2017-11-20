# -*- coding: utf-8 -*-

from flask_restplus import fields
from . import api

user_post = api.model('User post', {
    'username': fields.String(required=True, min_length=3, max_length=32, description='User unique name'),
    'password': fields.String(required=True, min_length=3, max_length=16, description='User password'),
    'email': fields.String(required=False, min_length=3, max_length=32, description='User email'),
})

user_patch = api.model('User patch', {
    'password': fields.String(required=False, min_length=3, max_length=16, description='User password'),
    'email': fields.String(required=False, min_length=3, max_length=32, description='User email'),
})

user_minimal = api.model('User minimal', {
    'id': fields.Integer(required=True, description='User unique id'),
    'username': fields.String(required=True, description='User username'),
    'created_at': fields.DateTime(required=True, description='User creation datetime'),
    'uri': fields.Url('admin.users_user_item')
})

user_detail = api.inherit('User details', user_minimal, {
    'email': fields.String(required=False, description='User emal')
})

user_data_container = api.model('User DataContainer', {
    'users': fields.List(fields.Nested(user_minimal))
})