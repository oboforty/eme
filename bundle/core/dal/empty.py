import uuid
from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, ForeignKey, ForeignKeyConstraint, Date, DateTime, \
    TIMESTAMP, func, Float
from sqlalchemy.orm import relationship

from core.ctx import EntityBase
from eme.data_access import GUID
from eme.data_access import Repository


class {class_name}(EntityBase):
    __tablename__ = '{table_name}'

    {class_capital}id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    def __init__(self, **kwargs):
        self.{class_capital}id = kwargs.get('{class_capital}id')
        self.created_at = kwargs.get('created_at')

    def to_dict(self):
        return {
            "{class_capital}id": self.{class_capital}id,
            "created_at": self.created_at,
        }

    def __repr__(self):
        return "{}".format(str(self.{class_capital}id)[0:4])


@Repository({class_name})
class {class_name}Repository(HeadRepository):
    pass
