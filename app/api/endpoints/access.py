# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.access import access_post, access_patch, access_minimal, access_data_container
from app.extensions import db
from app.models import User

ns = Namespace('access', description='Access related operations')

# ================================================================================================
# AUTH
# ================================================================================================
#
#   Auth verification
#
# ================================================================================================

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """
    Verify auth token

    :param token: User token
    :type token: str

    :return: True if valid token, else False
    :rtype: bool
    """
    user = User.verify_auth_token(token)

    if not user:
        return False

    g.user = user
    return True


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API clients endpoints
#
# ================================================================================================

@ns.route('/')
class AccessCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(access_data_container)
    def get(self):
        pass

    @ns.marshal_with(access_minimal, code=201, description='Access successfully added.')
    @ns.doc(response={
        404: 'Client not found'
    })
    @ns.expect(access_post)
    def post(self):
        pass


@ns.route('/<int:id>')
@ns.response(404, 'Access not found')
class AccessItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(access_minimal)
    def get(self, id):
        pass

    @ns.response(204, 'Access successfully patched.')
    @ns.expect(access_patch)
    def patch(self, id):
        pass

    @ns.response(204, 'Access successfully deleted.')
    def delete(self, id):
        pass
