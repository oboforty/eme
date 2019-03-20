from eme.entities import loadConfig
from eme.websocket import WebsocketApp


class ExampleServer(WebsocketApp):

    def __init__(self):
        conf = loadConfig('wsapp/config.ini')

        super().__init__(conf)


if __name__ == "__main__":
    app = ExampleServer()
    app.start()
