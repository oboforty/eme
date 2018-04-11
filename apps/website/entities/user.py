from flask_login import UserMixin

from bll.entities.user import User


class UserAuth(UserMixin, User):
    def __init__(self, user=None, **kwargs):
        if user and isinstance(user, User):
            User.__init__(self, **user.__dict__)
        else:
            User.__init__(self, **kwargs)
        self.id = self.uid
        self.validated = kwargs.get('validated')

    def __repr__(self):
        return "%s (%d)" % (self.email, self.uid)
