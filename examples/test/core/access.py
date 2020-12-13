import uuid


def verify(policy, user, entity=None):
    if user is None:
        return False
    elif 'admin' == policy:
        # we already determined that user is not an admin
        return hasattr(user, 'admin') and user.admin
    elif 'me' == policy:
        if isinstance(entity, str):
            entity = uuid.UUID(entity)

        if isinstance(entity, uuid.UUID):
            return user.uid == entity
        else:
            return user.uid == entity.uid
    elif 'owner' == policy:
        return entity is not None and entity.owner_id == user.uid
    elif 'guest' == policy:
        return user.is_authenticated
    elif 'anyone' == policy:
        return True
    else:
        raise Exception("Policy not found: {}".format(policy))
