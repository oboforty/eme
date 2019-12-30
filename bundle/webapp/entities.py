import json

from flask import Response
from flask_login import UserMixin

from core.dal.users import User
from eme.entities import EntityJSONEncoder



class ApiResponse(Response):

    def __init__(self, response=None, status=None, headers=None, direct_passthrough=False):
        jsonresp = json.dumps(response, cls=EntityJSONEncoder)

        super().__init__(response=jsonresp, status=status, headers=headers, direct_passthrough=direct_passthrough, mimetype='application/json')

        self.api = True


class UserAuth(UserMixin, User):
    def __init__(self, user: User):
        User.__init__(self, **user.__dict__)

        self.id = self.uid
        self.guest = False

    def __repr__(self):
        return "%s (%s)" % (self.email, self.uid)
