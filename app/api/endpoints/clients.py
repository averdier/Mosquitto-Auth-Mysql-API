# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.clients import client_post, client_patch, client_minimal, client_detail, client_data_container
from app.extensions import db
from app.models import User

ns = Namespace('clients', description='Clients related operations')

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
class ClientCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(client_data_container)
    def get(self):
        pass

    @ns.marshal_with(client_minimal, code=201, description='Client successfully added.')
    @ns.doc(response={
        409: 'Value exist'
    })
    @ns.expect(client_post)
    def post(self):
        pass


@ns.route('/<int:id>')
@ns.response(404, 'Client not found')
class ClientItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(client_detail)
    def get(self, id):
        pass

    @ns.response(204, 'Client successfully patched.')
    @ns.expect(client_patch)
    def patch(self, id):
        pass

    @ns.response(204, 'Client successfully deleted.')
    def delete(self, id):
        pass
