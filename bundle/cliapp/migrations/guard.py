from core.instance import users


def check_db():
    try:
        w = users.list_all()
        return not w
    except:
        pass

    return True

def clear_db():
    ww = worlds.list_all()

    users.delete_all()
    worlds.delete_all()
