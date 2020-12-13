import uuid

from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, ForeignKey, ForeignKeyConstraint, Date, DateTime, \
    TIMESTAMP, func, Float, Binary

from eme.data_access import GUID, JSON_GEN
from eme.data_access import Repository

from modules.
from core.ctx import EntityBase


class User(EntityBase):
    __tablename__ = 'users'

    uid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.now())
    last_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    # auth
    username = Column(String(32))
    email = Column(String(128))
    token = Column(String(128), nullable=True)

    salt = Column(Binary(60), nullable=True)
    password = Column(Binary(60))

    # BLL
    admin = Column(Boolean(), default=False)

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid')

        self.email = kwargs.get('email')
        self.username = kwargs.get('username')

        self.salt = kwargs.get('salt')
        self.password = kwargs.get('password')

        self.admin = kwargs.get('admin')
        self.token = kwargs.get('token')

        # data conversion
        if isinstance(self.uid, str):
            self.uid = uuid.UUID(self.uid)

    @property
    def view(self):
        # view by default has no face

        return {
            "uid": self.uid,
            "username": self.username,
            "admin": self.admin,
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

    def get_user_id(self):
        # used for oauth2
        return self.uid

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
