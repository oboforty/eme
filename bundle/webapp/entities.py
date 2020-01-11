import json

from flask import Response
from eme.entities import EntityJSONEncoder


class ApiResponse(Response):

    def __init__(self, response=None, status=None, headers=None, direct_passthrough=False):
        jsonresp = json.dumps(response, cls=EntityJSONEncoder)

        super().__init__(response=jsonresp, status=status, headers=headers, direct_passthrough=direct_passthrough, mimetype='application/json')

        self.api = True

