import configparser
import time
from datetime import datetime
from enum import Enum
from importlib import import_module
from json import JSONEncoder
from os import listdir
from os.path import splitext


def loadHandlers(ctx, dirType, prefix=None):
    cL = len(dirType)
    if prefix:
        path = prefix + dirType.lower() + 's'
        prefix = prefix.replace('/', '.') + "."
        if prefix[-1] == '.':
            prefix = prefix[:-1]
    else:
        path = dirType.lower() + 's'
        prefix = ""
    handlerNames = [splitext(f)[0] for f in sorted(listdir(path)) if
                splitext(f)[0][-cL:] == dirType]
    handlers = {}

    for moduleName in handlerNames:
        module = import_module(prefix + dirType.lower() + "s." + moduleName)
        handlerClass = getattr(module, moduleName)
        handler = handlerClass(ctx)
        handlers[moduleName[:-cL]] = handler

    return handlers

def loadConfig(file):
    config = configparser.ConfigParser()
    config.read(file)

    return config._sections

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EntityJSONEncoder(JSONEncoder):
    def default(self, obj):

        if (hasattr(obj, 'toDict')):
            return obj.toDict()
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, datetime):
            return time.mktime(obj.timetuple())
        #else:
        #    return obj.__dict__

        return JSONEncoder.default(self, obj)


class EntityPatch():
    def __init__(self, content=None, **kwargs):
        if not content:
            self.__dict__ = kwargs
        elif isinstance(content, dict):
            self.__dict__ = content
        else:
            self.__dict__ = content.__dict__

    def items(self):
        return self.__dict__.items()

    def toDict(self):
        return self.__dict__

    def toView(self):
        return EntityView(self, entityClass='Entity')


class EntityView():

    def __init__(self, entity, entityClass=None):
        self.entity = entity
        if entityClass is None:
            self.entityClass = self.__class__.__name__[:-4]
        else:
            self.entityClass = entityClass

    def toDict(self):
        _dict = dict(self.__dict__)

        for objName in dir(self):
            if objName.startswith('__') or objName == 'toDict':
                continue

            obj = _dict[objName]
            if objName == 'entity':
                del _dict[objName]
            elif isinstance(obj, set):
                _dict[objName] = list(obj)
            elif isinstance(obj, bytes):
                _dict[objName] = obj.decode("utf-8")
            elif isinstance(obj, EntityView):
                _dict[objName] = obj.toDict()
            elif isinstance(obj, list):
                subEntList = []
                for subEnt in obj:
                    if isinstance(subEnt, EntityView):
                        subEntList.append(subEnt.toDict())
                    else:
                        subEntList.append(subEnt)

                _dict[objName] = subEntList
            else:
                del _dict[objName]

        return _dict


