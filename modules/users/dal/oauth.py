import time

from eme.data_access import Repository, RepositoryBase, GUID
from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, ForeignKey, ForeignKeyConstraint, Date, DateTime, \
    TIMESTAMP, func, Float, Text, or_
from sqlalchemy.orm import relationship

from core.ctx import EntityBase
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)


class OAuth2Client(EntityBase, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    def __init__(self, **kwargs):
        self.client_id = kwargs.get('client_id')
        self.client_id_issued_at = kwargs.get('client_id_issued_at')
        self.user_id = kwargs.get('user_id')

    id = Column(Integer, primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.uid', ondelete='CASCADE'))
    user = relationship('User')


class OAuth2AuthorizationCode(EntityBase, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    def __init__(self, **kwargs):
        self.code = kwargs.get('code')
        self.client_id = kwargs.get('client_id')
        self.redirect_uri = kwargs.get('redirect_uri')
        self.scope = kwargs.get('scope')
        self.user_id = kwargs.get('user_id')

    id = Column(Integer, primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.uid', ondelete='CASCADE'))
    user = relationship('User')


class OAuth2Token(EntityBase, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = Column(Integer, primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.uid', ondelete='CASCADE'))
    user = relationship('User')

    def is_refresh_token_active(self):
        if self.revoked:
            return False

        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()


@Repository(OAuth2Client)
class ClientRepository(RepositoryBase):

    def find_auth_token_by_code(self, client_id, code):
        item = self.session.query(OAuth2AuthorizationCode)\
            .filter_by(code=code, client_id=client_id)\
            .first()

        return item

    def find_refresh_token(self, tk):
        t = self.session.query(OAuth2Token)\
            .filter_by(refresh_token=tk)\
            .first()

        return t

    def find_by_tag(self, client_id):
        client = self.session.query(OAuth2Client)\
            .filter_by(client_id=client_id)\
            .first()

        return client

    def list_tokens(self, client_id):
        tokens = self.session.query(OAuth2Token)\
            .filter_by(client_id=client_id)\
            .all()

        return tokens

    def list_codes(self, client_id):
        tokens = self.session.query(OAuth2AuthorizationCode) \
            .filter_by(client_id=client_id) \
            .all()

        return tokens

    def delete_expired(self):
        now = time.time()

        self.session.query(OAuth2Token) \
            .filter(OAuth2Token.expires_in+OAuth2Token.issued_at < now) \
            .delete()

        self.session.query(OAuth2AuthorizationCode) \
            .filter(OAuth2AuthorizationCode.auth_time+300 < now) \
            .delete()

        self.session.commit()

        return True
