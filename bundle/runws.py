from wsapp.server import MyWebsocketServer


app = MyWebsocketServer()


if __name__ == "__main__":
    # run it manually:
    app.start()
