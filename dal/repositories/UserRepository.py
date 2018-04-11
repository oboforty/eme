from bll.entities.user import User
from crudible.db import DbStore
from dal.ctx import dbctx


class UserRepository(DbStore):

    def __init__(self):
        super().__init__(ctx=dbctx)

        self.table = "users"
        self.primary = "uid"
        self.select = "*"
        self.insert = "email,password"
        self.update = ""
        self.entityType = User

