from eme.websocket import WSClient
#from game.entities import User


class UserWSGuest(User):
    def __init__(self, client: WSClient=None, **kwargs):
        User.__init__(self, **kwargs)

        self.id = kwargs.get('uid')
        self.client = client

    def __repr__(self):
        return "%s (%s)" % (self.username, self.uid)
