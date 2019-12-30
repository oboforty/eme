import json
import random
import string
import time
import bcrypt
import hashlib

from engine import settings
from game.entities import User


class UserException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return str(self.reason)


class UserManager:
    def __init__(self, repository):
        self.repository = repository

    def create(self, **userPatch):
        userPatch.update(json.loads(settings.get('auth.user', str, "{}")))

        raw_password = userPatch.pop('password')
        raw_password2 = userPatch.pop('password-confirm')

        user = User(**userPatch)

        # pw don't match
        if not raw_password == raw_password2:
            raise UserException('passwords_differ')
        # email exists
        if self.repository.find_user(email=user.email):
            raise UserException('email_exists')
        # username exists
        if self.repository.find_user(username=user.username):
            raise UserException('user_exists')

        # create user & pw salt
        user.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.salt = bcrypt.gensalt().decode('utf-8')
        user.token = self.getToken(user)
        self.repository.create(user)

        return user

    def getUser(self, uid):
        user = self.repository.find_user(uid)

        return user

    def authenticateToken(self, uid, token):
        user = self.repository.find_user(uid)
        if not user:
            raise UserException('user_doesnt_exist')

        # user
        if user.token == token:

            return user
        else:
            raise UserException('wrong_token')

    def authenticateCredentials(self, password, email=None, username=None):
        if email:
            user = self.repository.find_user(email=email)

            if not user:
                raise UserException('email_not_found')
        else:
            user = self.repository.find_user(username=username)

            if not user:
                raise UserException('user_not_found')

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user.token = self.getToken(user)
            self.repository.save()

            return user
        else:
            raise UserException('wrong_password')

    def authenticateCode(self, code):
        user = self.repository.find_user(code=code)

        return user

    def getToken(self, user):
        swd = '-'
        salt = str(user.uid) + swd + user.salt + "GPL2018v9$__SALUD" + str(time.time())
        token = hashlib.sha256(salt.encode('utf-8')).hexdigest()

        return token

    def forgot(self, nameOrEmail):
        user = self.repository.find_user(email=nameOrEmail)

        # #let's try with username
        # if not user:
        #     user = self.repository.find_user(name=nameOrEmail)

        if not user:
            return None

        N = 128
        code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

        user.forgot_code = code
        self.repository.save()

        return code

    def reset_password(self, code, raw_password, raw_password2):

        if not raw_password == raw_password2:
            raise UserException('passwords_differ')

        user = self.repository.find_user(code=code)

        if not user:
            raise UserException('wrong_code')

        user.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.salt = bcrypt.gensalt().decode('utf-8')
        user.token = self.getToken(user)
        user.forgot_code = None
        self.repository.save()

        return user
