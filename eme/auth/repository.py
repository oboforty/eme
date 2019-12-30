from ..data_access import RepositoryBase


class UserRepository(RepositoryBase):

    def find_user(self, uid=None, email=None, username=None, code=None):
        if uid is not None:
            return self.get(uid)

        sq = self.session.query(self.T)

        if username is not None:
            sq = sq.filter(self.T.username == username)
        elif email is not None:
            sq = sq.filter(self.T.email == email)
        elif code is not None:
            sq = sq.filter(self.T.forgot_code == code)
        else:
            return None

        return sq.first()
