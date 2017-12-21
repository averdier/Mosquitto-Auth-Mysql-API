# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.clients import client_post, client_patch, client_minimal, client_detail, client_data_container
from app.extensions import db
from app.models import User, MqttClient

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
        """
        Return mqtt clients list
        """

        return {'clients': MqttClient.query.all()}

    @ns.marshal_with(client_minimal, code=201, description='Client successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(client_post)
    def post(self):
        """
        Add mqtt client
        """
        data = request.json

        print(data)

        if MqttClient.query.filter_by(username=data['username']).first() is not None:
            abort(400, error='Username already exist')

        client = MqttClient()
        client.username = data['username']
        client.hash_password(data['password'])
        client.is_admin = data['is_admin']

        db.session.add(client)
        db.session.commit()

        return client, 201


@ns.route('/<int:id>')
@ns.response(404, 'Client not found')
class ClientItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(client_detail)
    def get(self, id):
        """
        Get client
        """
        client = MqttClient.query.get_or_404(id)

        return client

    @ns.response(204, 'Client successfully patched.')
    @ns.expect(client_patch)
    def patch(self, id):
        """
        Patch client
        """

        client = MqttClient.query.get_or_404(id)

        data = request.json

        patched = False
        if data.get('password', None) is not None:
            client.hash_password(data['password'])
            patched = True

        if data.get('is_admin', None) is not None:
            client.is_admin = data['is_admin']
            patched = True

        if patched:
            db.session.add(client)
            db.session.commit()

        return 'Client successfully patched.', 204

    @ns.response(204, 'Client successfully deleted.')
    def delete(self, id):
        """
        Delete client
        """

        client = MqttClient.query.get_or_404(id)

        db.session.delete(client)
        db.session.commit()

        return 'Client successfully deleted.', 204
