import random
import string
import time
import bcrypt
import hashlib


class AuthException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return str(self.reason)


def get_token(user, salt=''):
    swd = '-'
    salt = str(user.uid) + swd + user.salt + salt + str(time.time())
    token = hashlib.sha256(salt.encode('utf-8')).hexdigest()

    return token


class UserManager:
    def __init__(self, repository):
        self.repository = repository
        self.T = self.repository.T

    def create(self, **userPatch):
        raw_password = userPatch.pop('password')
        raw_password2 = userPatch.pop('password-confirm')

        user = self.T(**userPatch)

        # pw don't match
        if not raw_password == raw_password2:
            raise AuthException('passwords_differ')
        # email exists
        if self.repository.find_user(email=user.email):
            raise AuthException('email_exists')
        # username exists
        if self.repository.find_user(username=user.username):
            raise AuthException('user_exists')

        # create user & pw salt
        user.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.salt = bcrypt.gensalt().decode('utf-8')
        user.token = get_token(user)
        self.repository.create(user)

        return user

    def get_user(self, uid):
        return self.repository.find_user(uid)

    def get_by_credentials(self, password, email=None, username=None):
        if email:
            user = self.repository.find_user(email=email)

            if not user:
                raise AuthException('email_not_found')
        else:
            user = self.repository.find_user(username=username)

            if not user:
                raise AuthException('user_not_found')

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user.token = get_token(user)
            self.repository.save()

            return user
        else:
            raise AuthException('wrong_password')

    def get_by_token(self, uid, token):
        user = self.repository.find_user(uid)
        if not user:
            raise AuthException('user_doesnt_exist')

        if user.token == token:
            return user
        else:
            raise AuthException('wrong_token')

    def get_by_code(self, code):
        return self.repository.find_user(code=code)

    def request_forgot_code(self, email=None, username=None):
        if email is not None:
            user = self.repository.find_user(email=email)

            if not user and username is not None:
                user = self.repository.find_user(username=username)

            if not user:
                raise AuthException('email_not_found')
        elif username is not None:
            user = self.repository.find_user(username=username)

            if not user and email is not None:
                user = self.repository.find_user(email=email)

            if not user:
                raise AuthException('user_not_found')
        else:
            raise AuthException("provide_email_or_username")

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

    def reset_password(self, forgot_code, raw_password, raw_password2):

        if not raw_password == raw_password2:
            raise AuthException('passwords_differ')

        user = self.repository.find_user(code=forgot_code)

        if not user:
            raise AuthException('wrong_code')

        user.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.salt = bcrypt.gensalt().decode('utf-8')
        user.token = get_token(user)
        user.forgot_code = None
        self.repository.save()

        return user

    def logout(self):
        # todo: update last logout stamp?
        pass

    def activate_email(self, reg_code):
        # todo: ...
        pass
