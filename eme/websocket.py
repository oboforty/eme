import inspect
import json
import signal
from types import SimpleNamespace

import websockets
from websockets.protocol import State
import asyncio
import logging
import sys
from os.path import join


from eme.entities import load_handlers, EntityJSONEncoder


class EmeWebsocketClient(websockets.WebSocketServerProtocol):
    def __init__(self, **kwargs):
        self.user = None

        super().__init__(**kwargs)


class WebsocketApp():
    def __init__(self, config: dict, fbase='wsapp'):
        if len(config) == 0:
            raise Exception("Empty config file provided")
        conf = config['websocket']
        sys.path.append(fbase)

        self.host = conf.get('host', '0.0.0.0')
        self.port = conf.get('port')

        self.debug = conf.get('debug')

        # ws handler
        signal.signal(signal.SIGINT, self.close_sig_handler)
        self.clients = {}
        self.func_params = {}
        self.groups = load_handlers(self, "Group", conf.get('groups_dir'), prefix_path=fbase)

        # Logging
        logger = logging.getLogger(conf.get('logprefix', 'eme'))
        logger.setLevel(logging.DEBUG)

        # file log
        fh = logging.FileHandler(conf.get('logfile', join(fbase, 'logs.txt')))
        lvl = conf.get('loglevel', 'WARNING')
        fh.setLevel(getattr(logging, lvl))

        # console log
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

        self.logger = logger

    def close_sig_handler(self, signal, frame):
        self.close()

    def allow_message(self, route, rws):
        return True

    def build_request(self, ws, rws, route):
        return SimpleNamespace(route=route, data=rws, client=ws)

    async def handle_requests(self, websocket, path):
        async for message in websocket:
            rws = json.loads(message)

            # get action
            route = rws.pop("route", ':')
            group, method = route.split(":")
            groups = group.split('/')
            group = groups.pop(0)
            if len(groups) > 0:
                method = method + '_' + '_'.join(groups)

            if not self.allow_message(route, rws):
                return

            msid = rws.pop('msid', None)

            try:
                action = getattr(self.groups[group], method)
            except:
                logging.error("Route not found {}".format(route))

                if self.debug:
                    raise Exception("Route not found {}".format(route))
                return

            if route not in self.func_params:
                # find out what the function requires
                sig = inspect.signature(action)
                self.func_params[route] = list(sig.parameters.keys())

            param_names = self.func_params[route]
            params = {}

            if 'msid' in param_names:
                param_names['msid'] = msid

            if 'request' in param_names:
                params['request'] = self.build_request(websocket, rws, route)

            if 'user' in param_names:
                if not hasattr(websocket, 'user') or websocket.user is None:
                    # user authentication required, error
                    return None
                params['user'] = websocket.user
            if 'client' in param_names:
                params['client'] = websocket

            # execute function
            try:
                response = await action(**params)

                if response is not None:
                    await self.send(response, websocket, route=route, msid=msid)

            except Exception as e:
                logging.exception("METHOD")

                if self.debug:
                    raise e

    def start(self):
        print("Websocket: listening on {}:{}".format(self.host, self.port))

        asyncio.get_event_loop().run_until_complete(
            #  klass=EmeWebsocketClient
            websockets.serve(self.handle_requests, self.host, self.port))
        asyncio.get_event_loop().run_forever()

    def close(self):
        print("Exited websocket server")
        sys.exit()

    async def send(self, rws, client, route=None, msid=None):
        if client.state is State.CLOSED:
            return

        if isinstance(rws, dict):
            if route is not None:
                rws['route'] = route

            if msid is not None:
                rws['msid'] = msid

            await client.send(json.dumps(rws, cls=EntityJSONEncoder))
        elif isinstance(rws, str):
            await client.send(rws)
        elif isinstance(rws, list):
            for rw_ in rws:
                await self.send(rw_, client, route=route)
        else:
            raise Exception("Unsupported message type: {}".format(type(rws)))
