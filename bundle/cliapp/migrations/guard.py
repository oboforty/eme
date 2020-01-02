from core.dal.users import User
from eme.data_access import get_repo


def check_db():
    try:
        w = get_repo(User).is_empty()
        return not w
    except:
        pass

    return True

def clear_db():
    get_repo(User).delete_all()

    # implement your own calls to clear the database
