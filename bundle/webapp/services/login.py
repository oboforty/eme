import uuid

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from core.dal.users import User
from eme.data_access import get_repo

from webapp.entities import UserAuth

loginManager = LoginManager()
usersRepository = None


def init_login(server, conf):
    global loginManager, usersRepository

    server.config["SECRET_KEY"] = conf.get("secret_key")
    loginManager.init_app(server)
    loginManager.login_view = "get__users/login"

    usersRepository = get_repo(User)


@loginManager.user_loader
def load_user(uid):
    if uid is None:
        return None
    if uid == 'None':
        raise Exception("Very interesting UID provided")

    user = usersRepository.get(uid)

    if not user:
        user = User(uid=uuid.UUID(uid), username=None)

    if user.uid == 'None':

        raise Exception("ahusdjfsda asdk e ags sd gsrgsthr")

    return UserAuth(user)


def getUser() -> UserAuth:

    if not current_user.is_authenticated:
        # fetch anon user
        user = User(uid=uuid.uuid4(), username=None)

        setUser(UserAuth(user))

    return current_user


def forceAnonLogin(uid):
    anon = User(uid=uuid.uuid4(), username=None)

    setUser(anon)


def setUser(user, remember=True):
    assert not user.uid == 'None'
    if not isinstance(user, UserAuth):
        assert not user.uid == 'None'
        user = UserAuth(user)
        assert not user.uid == 'None'
    assert not user.uid == 'None'
    login_user(user, remember=remember)


def logout():
    logout_user()
