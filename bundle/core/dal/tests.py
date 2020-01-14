import uuid
from sqlalchemy import Column, TIMESTAMP, func, Float, Integer, Boolean, String
from sqlalchemy.orm import relationship

from core.ctx import EntityBase
from eme.data_access import Repository, RepositoryBase, GUID, JSON_GEN


class Test(EntityBase):
    __tablename__ = 'tests'
    wid = Column(String)
    yolo = Column(Integer, default=25)

    def __init__(self, **kwargs):
        self.wid = kwargs.get("wid")
        self.yolo = kwargs.get("yolo")

    def to_dict(self):
        return {
            "wid": self.wid,
            "yolo": self.yolo,
        }

    def __repr__(self):
        return str(self.tid)[0:4]


@Repository(Test)
class TestRepository(Repository):
    pass
