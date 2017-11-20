# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.users import user_data_container, user_minimal, user_detail, user_post, user_patch
from app.extensions import db
from app.models import User

ns = Namespace('users', description='Users related operations')

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

    if not user or not user.is_admin:
        return False

    g.user = user
    return True


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API users endpoints
#
# ================================================================================================

@ns.route('/')
class UserCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_data_container)
    def get(self):
        """
        Return users list
        """

        return {'users': User.query.all()}

    @ns.marshal_with(user_minimal, code=201, description='User successfully added.')
    @ns.doc(response={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(user_post)
    def post(self):
        """
        Add user
        """

        data = request.json

        if User.query.filter_by(username=data['username']).first() is not None:
            abort(400, error='Username already exist')

        user = User()
        user.username = data['username']
        user.hash_password(data['password'])
        user.is_admin = data['is_admin']

        if data.get('email', None) is not None:
            user.email = data['email']

        db.session.add(user)
        db.session.commit()

        return user, 201


@ns.route('/<int:id>')
@ns.response(404, 'User not found')
class UserItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_detail)
    def get(self, id):
        """
        Get user
        """

        user = User.query.get_or_404(id)

        return user

    @ns.response(204, 'User successfully patched.')
    @ns.doc(response={
        404: 'Account not found'
    })
    @ns.expect(user_patch)
    def patch(self, id):
        """
        Patch user
        """

        user = User.query.get_or_404(id)

        data = request.json

        patched = False
        if data.get('password', None) is not None:
            user.hash_password(data['password'])
            patched = True

        if data.get('email', None) is not None:
            user.email = data['email']
            patched = True

        if data.get('is_admin', None) is not None:
            user.is_admin = data['is_admin']
            patched = True

        if patched:
            db.session.add(user)
            db.session.commit()

        return 'User successfully patched', 204

    @ns.response(204, 'User successfully deleted.')
    def delete(self, id):
        """
        Delete user
        """
        user = User.query.get_or_404(id)

        db.session.delete(user)
        db.session.commit()

        return 'User successfully deleted.', 204