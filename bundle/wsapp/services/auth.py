from core.dal.users import User
from eme.auth import UserManager
from eme.data_access import get_repo

user_manager = None
user_repo = None


def init(app, conf):
    global user_repo, user_manager

    user_repo = get_repo(User)
    user_manager = UserManager(user_repo)
