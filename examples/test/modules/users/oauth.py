import os

from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector
from authlib.integrations.sqla_oauth2 import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.oauth2.rfc6749 import grants
from eme.data_access import get_repo
from werkzeug.security import gen_salt

from .dal.oauth import OAuth2Client, OAuth2AuthorizationCode, OAuth2Token, ClientRepository
from modules.users import auth

repo: ClientRepository = get_repo(OAuth2Client)


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def create_authorization_code(self, client, grant_user, request):
        code = gen_salt(48)
        item = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=grant_user.uid,
        )
        repo.create(item)

        return code

    def parse_authorization_code(self, code, client):
        item = repo.find_auth_token_by_code(client.client_id, code)

        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        repo.delete(authorization_code)

    def authenticate_user(self, authorization_code):
        # User.query.get()
        user = auth.user_repo.get(authorization_code.user_id)
        return user


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        is_email = '@' in username
        if is_email:
            user = auth.user_manager.get_by_credentials(password, email=username)
        else:
            user = auth.user_manager.get_by_credentials(password, username=username)

        if user is not None:
            return user


class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        token = repo.find_refresh_token(refresh_token)

        if token and token.is_refresh_token_active():
            return token

    def authenticate_user(self, credential):
        return auth.user_repo.get(credential.user_id)

    def revoke_old_credential(self, credential):
        credential.revoked = True

        repo.create(credential)


query_client = create_query_client_func(repo.session, OAuth2Client)
save_token = create_save_token_func(repo.session, OAuth2Token)
authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)
require_oauth = ResourceProtector()


def init(app, conf):
    global require_oauth, authorization

    if app.debug:
        # debug: disable SSL
        os.environ['AUTHLIB_INSECURE_TRANSPORT'] = 'true'

    # ----------------

    authorization.init_app(app)

    # support all grants
    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_grant(AuthorizationCodeGrant)
    authorization.register_grant(PasswordGrant)
    authorization.register_grant(RefreshTokenGrant)

    # support revocation
    revocation_cls = create_revocation_endpoint(repo.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)

    # protect resource
    bearer_cls = create_bearer_token_validator(repo.session, OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())
