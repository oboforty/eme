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