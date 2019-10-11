import configparser
import time
from datetime import datetime, date
from enum import Enum
from importlib import import_module
from json import JSONEncoder
from os import listdir
from os.path import splitext
from uuid import UUID


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
    handlerNames = [splitext(f)[0] for f in sorted(listdir(path)) if splitext(f)[0][-cL:] == dirType]
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

def loadSettings(file):
    conf = loadConfig(file)

    for okey, oval in conf.items():
        for key, val in oval.items():
            if val == 'yes':
                conf[okey][key] = True
            elif val == 'no':
                conf[okey][key] = False
            elif ',' in val:
                conf[okey][key] = val.split(',')

    return conf


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EntityJSONEncoder(JSONEncoder):
    def default(self, obj):

        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, datetime) or isinstance(obj, date):
            return time.mktime(obj.timetuple())
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, set) or isinstance(obj, list):
            return list(obj)
        elif isinstance(obj, bytes):
            return obj.decode("utf-8")
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
