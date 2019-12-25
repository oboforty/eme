import configparser
import os
import time
from datetime import datetime, date
from enum import Enum
from importlib import import_module
from json import JSONEncoder
from uuid import UUID


def load_handlers(ctx, dirType, path=None):
    cL = len(dirType)

    if path is None or not path:
        # smart-guess: path is local path + plural handler type
        path = dirType.lower() + 's'
        module_path = os.path.normpath(path)
    else:
        if os.path.isabs(path):
            # resolve absolute path to
            pathx = os.path.normpath(path).replace(os.path.normpath(os.getcwd()), '')
        else:
            pathx = os.path.normpath(path)
        module_path = pathx.replace("//", '.').replace("/", '.').replace('\\', '.')

    if module_path[0] == '.':
        module_path = module_path[1:]

    handlerNames = [os.path.splitext(f)[0] for f in sorted(os.listdir(path)) if os.path.splitext(f)[0][-cL:] == dirType]
    handlers = {}

    for moduleName in handlerNames:
        module = import_module(module_path + "." + moduleName)
        handlerClass = getattr(module, moduleName)
        handler = handlerClass(ctx)
        handlers[moduleName[:-cL]] = handler

    return handlers

def load_config(file):
    config = configparser.ConfigParser()
    config.read(file)

    return config._sections

def load_settings(file):
    conf = load_config(file)

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
