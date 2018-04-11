import bcrypt
import hashlib

from bll.entities.user import User
from dal.repositories.UserRepository import UserRepository


class UserException(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return str(self.code)


class UserManager():
    def __init__(self):
        self.repository = UserRepository()

    def create(self, userPatch):
        user = User(**userPatch)
        if not user.password == userPatch.get('password-confirm'):
            raise UserException(4)

        existingUser = self.repository.get(email=user.email)
        if existingUser:
            raise UserException(5)

        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.salt = bcrypt.gensalt().decode('utf-8')
        user.uid = self.repository.create(user)

        return user

    def getUser(self, uid):
        user = self.repository.get(uid)
        return user

    def authenticateToken(self, uid, token):
        user: User = self.repository.get(uid)
        if not user:
            raise UserException(1)

        if user.token == token:
            return user
        else:
            raise UserException(3)

    def authenticateCredentials(self, email, password):
        user: User = self.repository.getOne(email=email)

        if not user:
            raise UserException(1)

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # todo: perhaps delete sensitive data (UserBase class?)

            return user
        else:
            raise UserException(2)

    def createToken(self, user):
        user.token = self.getToken(user)
        self.repository.edit(user.uid, token=user.token)

        return user.token

    def getToken(self, user):
        swd = '-'
        # todo: no need to encode, just store everything in bytestring!
        salt = str(user.uid) + swd + user.salt + "GPL2018v4$__SALUD"
        token = hashlib.sha256(salt.encode('utf-8')).hexdigest()

        return token

