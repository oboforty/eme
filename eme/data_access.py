import json
import uuid
from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import TEXT
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID, JSONB


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class JSON_GEN(TypeDecorator):
    """Platform-independent JSONB type.
    Uses PostgreSQL's JSONB type, otherwise uses text
    """
    impl = TEXT

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(TEXT())

    def process_bind_param(self, value, dialect):
        # python -> DB conversion
        if value is None:
            return value

        if dialect.name == 'postgresql':
            return value
        else:
            if not isinstance(value, str):
                return json.dumps(value)
            return value

    def process_result_value(self, value, dialect):
        # DB -> python conversion
        if value is None:
            return value

        if dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, str):
                return json.loads(value)
            return value


class Repository(object):
    def __init__(self, type, register=True):
        self.type = type
        self.register = register

    def __call__(self, cls):
        class Wrapped(cls):
            cls.T = self.type

        if self.register:
            register_repository(self.type, cls)

        return Wrapped


class RepositoryBase:
    T = None

    def __init__(self, db_session):
        self.session: Session = db_session

    def get(self, eid):
        return self.session.query(self.T).get(eid)

    def count(self):
        return self.session.query(self.T).count()

    def is_empty(self):
        return bool(self.session.query(1).first())

    def list_all(self):
        return self.session.query(self.T).all()

    def save(self):
        self.session.commit()

    def create(self, ent, commit=True):
        self.session.add(ent)
        if commit:
            self.session.commit()

    def create_all(self, ents, commit=True):
        for ent in ents:
            self.session.add(ent)
        if commit:
            self.session.commit()

    def delete(self, ent, commit=True):
        self.session.delete(ent)
        if commit:
            self.session.commit()

    def delete_all(self, commit=True):
        self.session.query(self.T).delete()
        if commit:
            self.session.commit()


repositories = {}
sessions = {}


def register_session(type, sess):
    sessions[type] = sess


def register_repository(entClass, repoClass, type='db'):
    repositories[entClass] = repoClass(db_session=sessions[type])


def get_repo(entClass):
    if entClass not in repositories:
        raise Exception("Repository for {} is not registered!".format(entClass.__name__))

    return repositories[entClass]

