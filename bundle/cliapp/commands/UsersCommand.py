from core.dal.users import User
from eme.data_access import get_repo


class UsersCommand():
    def __init__(self, server):
        self.server = server
        self.users = get_repo(User)

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
        dusers = self.users.list_all()

        for user in dusers:
            print(user.uid, user.email, user.created_at)

    def runSetadmin(self, username):
        user = self.users.find_user(username=username)

        user.admin = not user.admin

        self.users.save()
        if user.admin:
            print("User is admin:", user.username, user.uid)
        else:
            print("User admin revoked:", user.username, user.uid)
