from eme.data_access import get_repo

from modules.users.dal.UserManager import UserManager
from modules.users.dal.entities.user import User


def create_testentities():
    user_repo = get_repo(User)
    user_manager = UserManager(user_repo)

    usrs = [
        ('admin', 'admin@example.com', 'admin', True),
    ]

    for username, email, pw, adm in usrs:
        user = user_manager.create(username=username, email=email, admin=adm, **{
            'password': pw,
            'password-confirm': pw
        })
