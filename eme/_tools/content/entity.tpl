import uuid
from sqlalchemy import Column, TIMESTAMP, func, Float, Integer, Boolean, String
from sqlalchemy.orm import relationship

from core.ctx import EntityBase
from eme.data_access import Repository, RepositoryBase, GUID, JSON_GEN


class {class_name}(EntityBase):
    __tablename__ = '{table_name}'{attr_def}

    def __init__(self, **kwargs):{attr_init}

    def to_dict(self):
        return {{{attr_view}
        }}

    def __repr__(self):
        return str(self.{eprefx}id)[0:4]


@Repository({class_name})
class {class_name}Repository(Repository):
    pass
