import datetime
import uuid
from time import time

from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, ForeignKey, ForeignKeyConstraint, Date, DateTime, \
    TIMESTAMP, func, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from eme.data_access import GUID, JSON_GEN

Base = declarative_base()


class World(Base):
    __tablename__ = 'worlds'

    # Worlds module
    wid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String(20))
    map = Column(String(20))
    max_players = Column(SmallInteger)

    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    invlink = Column(String(6))

    # Subentities
    users = relationship("User")
    areas = relationship("Area", cascade="delete")
    towns = relationship("Town", cascade="delete")

    def __init__(self, **kwargs):
        super().__init__()

        self.wid = kwargs.get('wid')
        self.name = kwargs.get('name')
        self.map = kwargs.get('map')
        self.max_players = kwargs.get('max_players')

        self.invlink = kwargs.get('invlink')
        self.last_update = kwargs.get('last_update', datetime.datetime.utcnow())

        if isinstance(self.wid, str):
            self.wid = uuid.UUID(self.wid)

    def to_dict(self):
        return {
            "wid": str(self.wid),
            "name": self.name,
            "map": self.map,
            "invlink": self.invlink,
            "max_players": self.max_players,
            "created_at": self.created_at,
            "last_update": self.last_update,
        }

    def __repr__(self):
        return "World({})".format(self.invlink)



class Town(Base):
    __tablename__ = 'towns'

    iso = Column(String(3), primary_key=True)
    wid = Column(GUID(), ForeignKey(World.wid), primary_key=True)
    name = Column(String(20))

    heightmap = Column(SmallInteger)

    # res_id -> lvl
    gatherers = Column(JSON_GEN())
    # res_id -> amount
    resources = Column(JSON_GEN())
    # build_id -> lvl
    buildings = Column(JSON_GEN())
    # build_id -> [x, y]
    placements = Column(JSON_GEN())

    # ORM
    world = relationship("World", back_populates="towns", viewonly=True)
    # __table_args__ = (ForeignKeyConstraint((iso, wid), [Country.iso, Country.wid]), {})

    def __init__(self, **kwargs):
        self.wid = kwargs.get('wid')
        self.iso = kwargs.get('iso')
        self.name = kwargs.get('name')

        self.heightmap = kwargs.get('heightmap')

        self.gatherers = kwargs.get('gatherers')
        self.resources = kwargs.get('resources')
        self.buildings = kwargs.get('buildings')
        self.placements = kwargs.get('placements')


        if isinstance(self.wid, str):
            self.wid = uuid.UUID(self.wid)


    def to_dict(self):
        return {
            "iso": self.iso,
            "name": self.name,
            "wid": str(self.wid),

            "heightmap": self.heightmap,

            "gatherers": self.gatherers,
            "resources": self.resources,
            "buildings": self.buildings,
            "placements": self.placements,
        }

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "Town #{}".format(self.iso)


class Area(Base):
    __tablename__ = 'areas'

    id = Column(String(8), primary_key=True)
    wid = Column(GUID(), ForeignKey(World.wid), primary_key=True)
    iso = Column(String(3))

    # ORM
    # world = relationship("World", back_populates="areas", viewonly=True)
    # __table_args__ = (ForeignKeyConstraint((iso, wid), [Country.iso, Country.wid]), {})

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.wid = kwargs.get('wid')
        self.iso = kwargs.get('iso')

        if isinstance(self.wid, str):
            self.wid = uuid.UUID(self.wid)

    def to_dict(self):
        return {
            "id": self.id,
            "iso": self.iso,
            "wid": str(self.wid),
        }

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "Area #{}".format(self.id)


class Warship(Base):
    __tablename__ = 'warships'

    id = Column(String(8), primary_key=True)

    # Placement
    wid = Column(GUID(), ForeignKey(World.wid), primary_key=True)
    iso = Column(String(3))
    lat = Column(Float(), nullable=True)
    lon = Column(Float(), nullable=True)

    # Attr
    name = Column(String(20))
    gold = Column(SmallInteger(), nullable=False)
    material_name = Column(String(), nullable=False)
    material_amount = Column(SmallInteger(), nullable=False)


    def __init__(self, **kwargs):

        self.id = kwargs.get('id')
        self.wid = kwargs.get('wid')
        self.iso = kwargs.get('iso')
        self.lat = kwargs.get('lat')
        self.lon = kwargs.get('lon')
        self.name = kwargs.get('name')

        self.gold = kwargs.get('gold')
        self.material_name = kwargs.get('materials_name')
        self.material_amount = kwargs.get('material_amount')
        self.trade_id = kwargs.get('trade_id')
        if isinstance(self.wid, str):
            self.wid = uuid.UUID(self.wid)

    def to_dict(self):
        return {
            "id": self.id,
            "wid": self.wid,
            "iso": self.iso,
            "lat": self.lat,
            "lon": self.lon,
            "name": self.name,
            "gold": self.gold,
            "material_name": self.material_name,
            "material_amount": self.material_amount,
            "trade_id": self.trade_id,
        }

    def __repr__(self):
        return "Ship{} ({},{})".format(self.name, self.lat, self.lon)


class Hero(Base):
    __tablename__ = 'heroes'

    id = Column(String(8), primary_key=True)

    # Placement
    wid = Column(GUID(), ForeignKey(World.wid), primary_key=True)
    iso = Column(String(3))
    area_id = Column(String(8), nullable=True)
    lat = Column(Float(), nullable=True)
    lon = Column(Float(), nullable=True)

    # Attr
    name = Column(String(20))
    face = Column(JSON_GEN())
    age = Column(SmallInteger())
    gold = Column(SmallInteger())

    # Fighting abilities
    health = Column(Float())
    xp_strength = Column(SmallInteger(), default=0)
    xp_leadership = Column(SmallInteger(), default=0)

    # Sub army
    hoplites = Column(SmallInteger(), default=0)
    skirmishers = Column(SmallInteger(), default=0)
    cavalry = Column(SmallInteger(), default=0)

    # Simulation
    doing = Column(String(5))
    doing_iter = Column(SmallInteger())
    happy = Column(Float())


    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.wid = kwargs.get('wid')
        self.iso = kwargs.get('iso')
        self.area_id = kwargs.get('area_id')
        self.lat = kwargs.get('lat')
        self.lon = kwargs.get('lon')
        self.name = kwargs.get('name')
        self.face = kwargs.get('face')
        self.age = kwargs.get('age')
        self.gold = kwargs.get('gold')
        self.health = kwargs.get('health')
        self.xp_strength = kwargs.get('xp_strength')
        self.xp_leadership = kwargs.get('xp_leadership')
        self.hoplites = kwargs.get('hoplites')
        self.skirmishers = kwargs.get('skirmishers')
        self.cavalry = kwargs.get('cavalry')
        self.doing = kwargs.get('doing')
        self.doing_iter = kwargs.get('doing_iter')
        self.happy = kwargs.get('happy')

        if isinstance(self.wid, str):
            self.wid = uuid.UUID(self.wid)

    def to_dict(self):
        return {
            "id": self.id,
            "wid": self.wid,
            "iso": self.iso,
            "area_id": self.area_id,
            "lat": self.lat,
            "lon": self.lon,
            "name": self.name,
            "face": self.face,
            "age": self.age,
            "gold": self.gold,
            "health": self.health,
            "xp_strength": self.xp_strength,
            "xp_leadership": self.xp_leadership,
            "hoplites": self.hoplites,
            "skirmishers": self.skirmishers,
            "cavalry": self.cavalry,
            "doing": self.doing,
            "doing_iter": self.doing_iter,
            "happy": self.happy,
        }

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "{}(age{} hp{} str{} gold{})".format(self.name, self.age, round(100*self.health), self.strength, self.gold)
