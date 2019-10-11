import json
import logging
import signal
import sys

from .vendor.websocket import SimpleWebSocketServer, WebSocket
from .entities import loadHandlers, EntityJSONEncoder, EntityPatch


class WSClient(WebSocket):
    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)
        self.user = None
        self.last_msid = None
        self.msid = None

    def handleMessage(self):
        self.server.message_received(self, self.data)

    def handleError(self, e):
        self.server.message_error(self, e)

    def handleConnected(self):
        self.server.client_connected(self)

    def handleClose(self):
        self.server.client_left(self)


class WebsocketApp(SimpleWebSocketServer):

    def __init__(self, config: dict):
        conf = config['websocket']
        crou = config['routing']
        chead = config['headers']

        # Socket
        self.host = conf.get('host')
        self.port = int(conf.get('port'))
        self.debug = conf.get('debug') == 'yes'

        # Clients
        self.clients = {}
        self.cliN = 0
        self.no_auth = set()

        # Routing
        self.addRouting(crou)

        # Groups
        self.groups = loadHandlers(self, "Group", prefix=conf.get('groups_folder'))

        # Logging
        if not conf.get('debug'):
            logging.basicConfig(filename=conf.get('log_file'), level=logging.WARNING)
            formatter = logging.Formatter(conf.get('log_format', '%(asctime)s %(levelname)s %(message)s'))
            logger = logging.getLogger(conf.get('log_prefix', 'web'))
            logger.addHandler(formatter)

            logging.info("Geopoly: {}:{}".format(self.host, self.port))

        else:
            print("Geopoly: Listening on port %d for clients.." % self.port)

        super().__init__(port=self.port, host=self.host, websocketclass=WSClient)
        signal.signal(signal.SIGINT, self.close_sig_handler)

    def close_sig_handler(self, signal, frame):
        self.close()
        sys.exit()

    def client_connected(self, client):
        if not self.debug:
            logging.info(str(client.address) + ' connected')

        client.id = self.cliN
        self.clients[client.id] = client
        self.cliN += 1

    def client_left(self, client):
        if not self.debug:
            logging.info(str(client.address) + ' left')

        del self.clients[client.id]

    def message_received(self, client, message):
        if not self.debug:
            logging.info(">" + message)
        rws = json.loads(message)

        authorize_req = rws['route'] not in self.no_auth
        if not client.user and authorize_req:
            print("Auth failed")
            return

        # get action
        route = rws.pop("route", ':')
        group, method = route.split(":")
        groups = group.split('/')
        group = groups.pop(0)
        if len(groups) > 0:
            method = method + '_' + '_'.join(groups)

        msid = rws.pop('msid', None)
        client.msid = msid
        if msid:
            client.last_msid = msid

        action = getattr(self.groups[group], method)

        params = self._forgeParams(rws)
        if authorize_req:
            params['user'] = client.user
        else:
            params['client'] = client
        try:
            response = action(**params)

            # automatic sending of response message (HTTP-like response for request)
            if isinstance(response, dict):
                if 'route' not in response:
                    response['route'] = route
                if msid is not None:
                    response['msid'] = msid

                self.send(response, client)
            elif isinstance(response, list):
                for resp in response:
                    if 'route' not in resp:
                        resp['route'] = route
                    if msid is not None:
                        resp['msid'] = msid
                    self.send(resp, client)

        except Exception as e:
            logging.exception("METHOD")

            if self.debug:
                print(e)
                raise e  # does not work because vendor is shit

    def dispose(self):
        if not self.debug:
            logging.info("Server exited")

    def send(self, rws, client):
        # send to client
        if isinstance(client, int):
            if client not in self.clients:
                return
            client = self.clients[client]

        client.sendMessage(json.dumps(rws, cls=EntityJSONEncoder))

    def broadcast(self, rws):
        # broadcast message
        for clientId, client in self.clients.items():
            client.sendMessage(json.dumps(rws, cls=EntityJSONEncoder))

    def sendRaw(self, rwsJSON, client):
        client.sendMessage(rwsJSON)

    def _forgeParams(self, rws):
        params = {}
        for param, val in rws.items():
            if isinstance(val, dict):
                params[param] = EntityPatch(val)
            elif isinstance(val, list):
                params[param] = []
                for elem in val:
                    if isinstance(elem, dict):
                        params[param].append(self._forgeParams(elem))
                    else:
                        params[param].append(elem)
            else:
                params[param] = val

        return params

    def addRouting(self, routing):
        for route, policy in routing.items():

            if policy == 'guest':
                self.no_auth.append(route)

    def start(self):
        self.serveforever()

    def message_error(self, client, e):
        print(e)

        if not self.debug:
            logging.exception("Server")

