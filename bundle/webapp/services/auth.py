import uuid

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from eme.auth import UserManager, login_forbidden
from eme.data_access import get_repo

from core.dal.users import User
from webapp.entities import UserAuth

login_manager = LoginManager()
user_manager = None
user_repo = None


def init(app, conf):
    global user_repo, user_manager, login_manager

    app.config["SECRET_KEY"] = conf.get("secret_key")

    login_manager.init_app(app)
    login_manager.login_view = "get__users/login"

    user_repo = get_repo(User)
    user_manager = UserManager(user_repo)

    app.jinja_env.globals.update(get_user=get_user)


@login_manager.user_loader
def load_user(uid):
    if uid is None:
        return None
    if uid == 'None':
        raise Exception("Very interesting UID provided")

    user = user_repo.get(uid)

    if not user:
        user = User(uid=uuid.UUID(uid), username=None)

    if user.uid == 'None':

        raise Exception("ahusdjfsda asdk e ags sd gsrgsthr")

    return UserAuth(user)


def get_user() -> UserAuth:

    if not current_user.is_authenticated:
        # fetch anon user
        user = User(uid=uuid.uuid4(), username=None)

        set_user(UserAuth(user))

    return current_user


def auth_guest(uid=None):
    anon = User(uid=uuid.uuid4(), username=None)

    set_user(anon)


def set_user(user, remember=True):
    assert not user.uid == 'None'
    if not isinstance(user, UserAuth):
        assert not user.uid == 'None'
        user = UserAuth(user)
        assert not user.uid == 'None'
    assert not user.uid == 'None'
    login_user(user, remember=remember)


def logout():
    user_manager.logout()
    logout_user()
