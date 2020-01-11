from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from eme.auth import UserManager, login_forbidden
from eme.data_access import get_repo

from core.dal.users import User
from flask_login import UserMixin


login_manager = LoginManager()
user_manager = None
user_repo = None


def init(app, conf):
    global user_repo, user_manager, login_manager

    app.config["SECRET_KEY"] = conf.get("secret_key")

    login_manager.init_app(app)
    #login_manager.login_view = "Users.get_login"

    user_repo = get_repo(User)
    user_manager = UserManager(user_repo)


@login_manager.user_loader
def load_user(uid):
    if uid is None or uid == 'None':
        return None

    return user_repo.get(uid)


def logout():
    user_manager.logout()
    logout_user()
