import time
import bcrypt
import hashlib

from core.entities import Player
from core.instance import players


class UserException(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return str(self.code)


class UserManager():
    def __init__(self):
        pass

    def create(self, userPatch):
        user = Player(**userPatch)

        if not user.password == userPatch.get('password-confirm'):
            raise UserException(4)

        existingUser = players.get(email=user.email)
        if existingUser:
            raise UserException(5)

        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.salt = bcrypt.gensalt().decode('utf-8')
        user.token = self.getToken(user)
        user.id = players.create(user)
        user.reg = True

        return user

    def getUser(self, uid) -> Player:
        user = players.get(uid)
        user.reg = True
        return user

    def authenticateToken(self, uid, token):
        user: Player = players.get(uid)
        if not user:
            raise UserException(1)

        # user
        if user.token == token:
            user.reg = True

            return user
        else:
            raise UserException(3)

    def authenticateCredentials(self, nameOrEmail, password):
        user: Player = players.getOne(email=nameOrEmail)

        if not user:
            # let's try with username
            user: Player = players.getOne(name=nameOrEmail)

        if not user:
            raise UserException(1)

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # todo: perhaps delete sensitive data (UserBase class?)
            user.token = self.getToken(user)

            players.edit(user.id, token=user.token, timestamp=False)
            user.reg = True
            return user
        else:
            raise UserException(2)

    # def authenticateFingerprint(self, uid):
    #     user: Player = self.cache.get(uid)
    #     user.reg = False
    #
    #     return user
    #
    # def createGuest(self, uid):
    #     user: Player = self.cache.get(uid)
    #
    #     if not user:
    #         user = EntityPatch(uid=uid)
    #         # todo: later: don't save all data just uid
    #         #user = Player(uid=uid)
    #         self.cache.create(user)
    #
    #         return user
    #     return False

    def getToken(self, user: Player):
        swd = '-'
        # todo: no need to encode, just store everything in bytestring!
        salt = str(user.id) + swd + user.salt + "GPL2018v9$__SALUD" + str(time.time())
        token = hashlib.sha256(salt.encode('utf-8')).hexdigest()

        return token
