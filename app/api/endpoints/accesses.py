# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.accesses import access_post, access_patch, access_minimal, access_data_container
from app.extensions import db
from app.models import User, MqttAccess, MqttClient

ns = Namespace('accesses', description='accesses related operations')

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
#   API accesses endpoints
#
# ================================================================================================

@ns.route('/')
class AccessCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(access_data_container)
    def get(self):
        """
        Return list of mqtt access
        """
        return {'accesses': MqttAccess.query.all()}

    @ns.marshal_with(access_minimal, code=201, description='Access successfully added.')
    @ns.doc(response={
        404: 'Client not found'
    })
    @ns.expect(access_post)
    def post(self):
        """
        Add mqtt access to user
        """
        data = request.json

        client = MqttClient.query.filter_by(username=data['username']).first()
        if client is None:
            abort(404, error='Client not found')

        access = MqttAccess()
        access.username = data['username']
        access.topic = data['topic']
        access.access = data['access']

        db.session.add(access)
        db.session.commit()

        return access, 201


@ns.route('/<int:id>')
@ns.response(404, 'Access not found')
class AccessItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(access_minimal)
    def get(self, id):
        """
        Get mqtt access
        """
        access = MqttAccess.query.get_or_404(id)

        return access

    @ns.response(204, 'Access successfully patched.')
    @ns.expect(access_patch)
    def patch(self, id):
        """
        Patch mqtt access
        """
        access = MqttAccess.query.get_or_404(id)

        data = request.json

        patched = False
        if data.get('topic', None) is not None:
            access.topic = data['topic']
            patched = True

        if data.get('access', None) is not None:
            access.access = data['access']
            patched = True

        if patched:
            db.session.add(access)
            db.session.commit()

        return 'Access successfully patched.', 204

    @ns.response(204, 'Access successfully deleted.')
    def delete(self, id):
        """
        Delete mqtt access
        """

        access = MqttAccess.query.get_or_404(id)

        db.session.delete(access)
        db.session.commit()


        return 'Access successfully deleted.', 204
