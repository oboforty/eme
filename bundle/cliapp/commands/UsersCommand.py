from core.instance import users


class UsersCommand():
    def __init__(self, server):
        self.server = server

        self.commands = {
            'users:list': {
                'help': 'Lists users',
                'short': {},
                'long': []
            },
            'users:setadmin': {
                'help': 'Sets admin',
                'short': {},
                'long': ['username=']
            },
        }

    def runList(self):
        dusers = users.list_all()

        for user in dusers:
            print(user.uid, user.email, user.created_at)

    def runSetadmin(self, username):
        user = users.find_user(username=username)

        user.admin = not user.admin

        users.save()
        if user.admin:
            print("User is admin:", user.username, user.uid)
        else:
            print("User admin revoked:", user.username, user.uid)
