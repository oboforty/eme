from eme.entities import loadConfig

from eme.tcpserver import TCPServerApp


class ExampleChat(TCPServerApp):


    def __init__(self):
        # eme/examples/simple_website is the working directory.
        conf = loadConfig('chatapp/config.ini')

        super().__init__(conf)