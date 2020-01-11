import datetime
import uuid
from time import time

from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, ForeignKey, ForeignKeyConstraint, Date, DateTime, \
    TIMESTAMP, func, Float
from sqlalchemy.orm import relationship

from core.ctx import EntityBase
from eme.data_access import GUID, JSON_GEN
from eme.auth.repository import UserRepositoryBase
from eme.data_access import Repository


class User(EntityBase):
    __tablename__ = 'users'

    uid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    last_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    username = Column(String(32))
    email = Column(String(128))
    salt = Column(String(128), nullable=True)
    token = Column(String(128), nullable=True)
    password = Column(String(128))
    admin = Column(Boolean(), default=False)

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid')

        self.email = kwargs.get('email')
        self.username = kwargs.get('username')

        self.salt = kwargs.get('salt')
        self.token = kwargs.get('token')
        self.password = kwargs.get('password')
        self.admin = kwargs.get('admin')

        # data conversion
        if isinstance(self.uid, str):
            self.uid = uuid.UUID(self.uid)

    def to_dict(self):
        return {
            "uid": self.uid,
            "username": self.username,
            "token": self.token,
        }

    def get_id(self):
        return str(self.uid) if self.uid else None

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.uid is not None

    @property
    def is_anonymous(self):
        return False

    def __hash__(self):
        return hash(self.uid)

    def __repr__(self):
        return "{}({}..)".format(self.username, str(self.uid)[0:4])


@Repository(User)
class UserRepository(UserRepositoryBase):

    def list_some(self, N):
        return self.session.query(User)\
            .limit(N)\
        .all()

    def delete_all_test(self):
        self.session.query(User)\
            .filter(User.username.like('___TEST___%'))\
        .delete(synchronize_session=False)
        self.session.commit()
