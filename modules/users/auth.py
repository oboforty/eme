from functools import wraps

from flask import current_app, request
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from eme.data_access import get_repo

from flask_login import UserMixin

from .dal.UserManager import UserManager
from .dal.entities.user import User

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


def login_forbidden(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
