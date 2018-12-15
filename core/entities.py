from enum import Enum

from flask_login import UserMixin

from core.entities import Player


class UserAuth(Player):
    def __init__(self, user: Player=None, **kwargs):
        if user and isinstance(user, Player):
            Player.__init__(self, **user.__dict__)
        else:
            Player.__init__(self, **kwargs)

        self.validated = kwargs.get('validated')
        self.authenticated = kwargs.get('authenticated')
        self.active = kwargs.get('active', True)

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "%s (%d)" % (self.email, self.id)
