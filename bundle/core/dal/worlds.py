import uuid
from sqlalchemy import Column, TIMESTAMP, func, Float, Integer, Boolean, String
from sqlalchemy.orm import relationship

from core.ctx import EntityBase
from eme.data_access import RepositoryBase, GUID, JSON_GEN, Repository


class World(EntityBase):
    __tablename__ = 'worlds'
    name = Column(String, default="Hellas")
    age = Column(Integer, default=10)

    def __init__(self, **kwargs):
        self.wid = kwargs.get("wid")
        self.name = kwargs.get("name")
        self.age = kwargs.get("age")

    def to_dict(self):
        return {
            "wid": self.wid,
            "name": self.name,
            "age": self.age,
        }

    def __repr__(self):
        return str(self.wid)[0:4]


@Repository(World)
class WorldRepository(Repository):
    pass
