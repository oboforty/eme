from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from flask import render_template, request
from flask_login import current_user

from modules.eme_utils.responses import ApiResponse
from modules.users import auth, oauth
from modules.users.oauth import require_oauth


class OauthController():
    def __init__(self, server):
        self.server = server

        self.server.preset_endpoints({
            'GET /me': 'Users.get_index',
            'GET /profile': 'Users.get_index',
         })

    @require_oauth('profile')
    def get_me(self):
        user = current_token.user

        if 'token' in request.args:
            # include user tokens
            view = user.view
            view['access_token'] = current_token.access_token
            view['refresh_token'] = current_token.refresh_token
            view['expires_in'] = current_token.expires_in
            view['issued_at'] = current_token.issued_at

            return ApiResponse(view)

        return ApiResponse(user.view)

    @auth.login_required
    def get_authorize(*args, **kwargs):
        user = current_user

        try:
            grant = oauth.authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error

        return render_template('/oauth/authorize.html', grant=grant)

    @auth.login_required
    def post_authorize(*args, **kwargs):
        user = current_user

        if not user and 'username' in request.form:
            username = request.form.get('username')

            user = auth.user_repo.find_user(username=username)
        if request.form['confirm']:
            grant_user = user
        else:
            grant_user = None

        return oauth.authorization.create_authorization_response(grant_user=grant_user)
        #return render_template('oauth/authorize.html', **kwargs)

    def post_token(self):
        return oauth.authorization.create_token_response()

    def post_revoke(self):
        return oauth.authorization.create_endpoint_response('revocation')
