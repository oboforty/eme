import uuid
from sqlalchemy import Column, TIMESTAMP, func, Float, Integer, Boolean, String
from sqlalchemy.orm import relationship

from core.ctx import EntityBase
from eme.data_access import Repository, RepositoryBase, GUID, JSON_GEN


class Guy(EntityBase):
    __tablename__ = 'guys'
    name = Column(String, default="Anon")
    age = Column(Integer, default=10)

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.age = kwargs.get("age")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
        }

    def __repr__(self):
        return str(self.gid)[0:4]


@Repository(Guy)
class GuyRepository(Repository):
    pass
