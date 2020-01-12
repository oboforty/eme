from unittest.mock import MagicMock, patch

import flask
from eme.entities import load_handlers, EntityPatch
from flask import request

from webapp.entities import ApiResponse

obj_webapp = MagicMock()
controllers = load_handlers(obj_webapp, "Controller", "webapp/")

obj_serverapp = MagicMock()
groups = load_handlers(obj_serverapp, "Group", "serverapp/")


def mock_http(controller_action, form_data=None, **kwargs):
    controller, action = controller_action.split(':')
    print("  >{}:{} {}".format(controller, action, kwargs))

    if form_data:
        request_mock = patch.object(flask, "request")

        with patch('request.form') as mock:
            mock.return_value = form_data

    resp = getattr(controllers[controller], action)(**kwargs)

    if resp:
        if isinstance(resp, ApiResponse):
            return resp.json

        return resp


def mock_ws(route, params, user=None, resp_format='dict'):
    group, action = route.split(':')
    print("  >{}:{} {}".format(group, action, params))
    if user is not None:
        params['user'] = user

    if resp_format == 'dict':
        clist = {
            "response": [],
            "broadcast": [],
            "to_user": [],
            "hall": [],
        }
        obj_serverapp.send.side_effect = lambda rws, cli: clist['to_user'].append(rws)
        obj_serverapp.send_to_world.side_effect = lambda wid, rws: clist['broadcast'].append(rws)
        obj_serverapp.send_to_hall.side_effect = lambda wid, rws: clist['hall'].append(rws)
        resp = getattr(groups[group], action)(**params)

        if resp:
            clist['response'].append(resp)
            clist['to_user'].append(resp)
    else:
        # store responses as list
        clist = []

        obj_serverapp.send.side_effect = lambda rws, cli: clist.append(rws)
        obj_serverapp.send_to_world.side_effect = lambda wid, rws: clist.append(rws)
        obj_serverapp.send_to_hall.side_effect = lambda wid, rws: clist.append(rws)
        resp = getattr(groups[group], action)(**params)

        if resp:
            clist.append(resp)
            clist.append(resp)

    return clist
