from time import time

from sqlalchemy import Column, TIMESTAMP, func, Boolean, SmallInteger, String, Integer
from flask_login import UserMixin as FlaskUserMixin
from eme.data_access import GUID, JSON_GEN


class UserMixin(FlaskUserMixin):
    # login
    uid = Column(GUID(), primary_key=True)
    username = Column(String(32))

    # profile
    admin = Column(Boolean(), default=False)
    last_active = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    # oauth
    access_token = Column(String(255), unique=True, nullable=False)
    refresh_token = Column(String(255), index=True)
    issued_at = Column(Integer, nullable=False, default=lambda: int(time()))
    expires_in = Column(Integer, nullable=False, default=0)


    def get_id(self):
        return str(self.uid) if self.uid else None

    @property
    def expires_at(self):
        if self.issued_at is None or self.expires_in is None:
            # bugfix for records that have no expiry
            return 0

        return self.issued_at + self.expires_in

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.uid is not None

    @property
    def is_anonymous(self):
        return False

    def get_user_id(self):
        # used for oauth2
        return self.uid

    def __hash__(self):
        return hash(self.uid)

    def __repr__(self):
        return "{}({}..)".format(self.username, str(self.uid)[0:4])

    def update_token(self, th):
        self.access_token = th.access_token
        self.issued_at = th.issued_at
        self.expires_in = th.expires_in

        if hasattr(th, 'refresh_token'):
            self.refresh_token = th.refresh_token

    def update_user(self, user):
        if self.access_token != user.access_token and user.access_token is not None:
            self.update_token(user)

        if hasattr(user, 'refresh_token'):
            self.refresh_token = user.refresh_token

        if user.username != self.username and user.username is not None:
            self.username = user.username

        if user.admin != self.admin and user.admin is not None:
            self.admin = user.admin

        if user.last_active != self.last_active and user.last_active is not None:
            self.last_active = user.last_active

