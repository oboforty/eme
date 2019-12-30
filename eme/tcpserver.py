import logging
#import socket
import socketserver

from eme.entities import loadHandlers


class TCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(self, request, client_address, server)

    def handle(self):
        data = self.request.recv()

        # todo: itt: to json, rws parse, response
        #self.server.send()

        return



class TCPServerApp(socketserver.TCPServer):

    def __init__(self, config: dict):
        conf = config['server']
        #crou = config['routing']

        # Socket
        self.host = conf.get('host')
        self.port = conf.get('port')
        self.poll_interval = conf.get('poll_interval', 0.5)

        super().__init__(self.host+':'+self.port, TCPHandler)

        # Controllers
        #self.manualRoutes = {}
        self.controllers = loadHandlers(self, "Group", prefix=conf.get('groups_folder'))

        # Logging
        logging.basicConfig(filename=conf.get('log_file'), level=logging.WARNING)
        formatter = logging.Formatter(conf.get('log_format', '%(asctime)s %(levelname)s %(message)s'))
        logger = logging.getLogger(conf.get('log_prefix', 'web'))
        logger.addHandler(formatter)

    def start(self):
        self.serve_forever(self.poll_interval)
