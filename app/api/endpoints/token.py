# -*- coding: utf-8 -*-

from flask import g
from flask_restplus import Namespace, Resource
from flask_httpauth import HTTPBasicAuth
from ..serializers import auth_token
from app.models import User

ns = Namespace('token', description='Token related operations')

# ================================================================================================
# AUTH
# ================================================================================================
#
#   Auth verification
#
# ================================================================================================

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """
    Verify User authorization

    :param username: Unique username
    :type username: str

    :param password: User password
    :type password: str

    :return: True if user can connect, else False
    :rtype: bool
    """

    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return False

    g.user = user
    return True


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API token endpoints
#
# ================================================================================================


@ns.route('/')
class TokenResource(Resource):
    decorators = [auth.login_required]

    @ns.doc(security='basicAuth')
    @ns.marshal_with(auth_token)
    def get(self):
        """
        Return auth token
        """

        token = g.user.generate_auth_token()

        return {'token': token.decode('ascii')}
