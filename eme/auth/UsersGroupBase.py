from eme.websocket import WSClient

from .UserManager import UserManager
from .entities import UserWSGuest


class UsersGroupBase:
    def __init__(self, server, users):
        self.server = server
        self.name = 'Users'

        self.server.no_auth.add('Users:auth_token')
        self.server.no_auth.add('Users:guest')

        self.userManager = UserManager(users)

    def guest(self, uid, iso, username, wid, client: WSClient):

        client.user = UserWSGuest(client, iso=iso, uid=uid, username=username, wid=wid)

        self.server.do_reconnect(client)

        return {
            "result": "OK"
        }

    def auth_token(self, uid, token, client: WSClient):
        # unsafe auth; replace later with oauth2
        user = self.userManager.authenticateToken(uid, token)

        if user:
            client.user = UserWSGuest(client, iso=user.iso, uid=uid, username=user.username, wid=user.wid)

            self.server.do_reconnect(client)

            return {
                "result": "OK"
            }
