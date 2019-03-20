from eme.websocket import WebsocketApp, WSClient

from wsapp.entities import User


class ChatGroup:

    def __init__(self, server):
        self.server: WebsocketApp = server
        self.group = 'Chat'

        self.history = []

        # This is another way to configure routes that do not require authentication
        self.server.no_auth.update([
            'Chat:register'
        ])

    def register(self, username: str, client: WSClient):
        # create new user object (normally we should authenticate with oauth2 or other means!)
        client.user = User(username=username, client=client)

        # by adding user attribute, the client will be able to access routes that require authentication

        self.server.broadcast({
            "route": "Chat:new_user",
            "username": username
        })

        # send history only to the new client:
        # you can specify route here too, but if you don't the same route will be used
        return {
            "username": username,
            "history": self.history
        }

    def message(self, msg: str, user: User):
        self.history.append(user.username + ': ' + msg)

        self.server.broadcast({
            "route": "Chat:new_message",
            "username": user.username,
            "msg": msg
        })
