import configparser
import os
import time
from datetime import datetime, date
from enum import Enum
from importlib import import_module
from json import JSONEncoder
from uuid import UUID

import inflect


def load_handlers(ctx, class_name, path=None, prefix_path=None):

    if path is None:
        # smart-guess: plural handler type
        p = inflect.engine()
        path = p.plural_noun(class_name).lower()

    module_path = path.replace(os.sep, '.').lstrip('.').rstrip('.')

    if prefix_path is not None:
        path = os.path.join(prefix_path, path)

    handlerNames = [os.path.splitext(f)[0] for f in sorted(os.listdir(path)) if f.endswith(class_name+'.py')]
    handlers = {}

    for moduleName in handlerNames:
        module = import_module(module_path + "." + moduleName)
        handlerClass = getattr(module, moduleName)
        handler = handlerClass(ctx)
        handlers[moduleName[:-len(class_name)]] = handler

    return handlers

def load_config(file):
    config = configparser.ConfigParser()
    config.read(file)

    return config._sections


def load_settings(file):
    conf = load_config(file)

    for okey, oval in conf.items():
        for key, val in oval.items():
            if val.lower() in ('yes', 'true'):
                conf[okey][key] = True
            elif val.lower() in ('no', 'false'):
                conf[okey][key] = False
            elif ',' in val:
                conf[okey][key] = val.split(',')

    return SettingWrapper(conf)


class SettingWrapper:
    def __init__(self, conf):
        self.conf = conf

    def __getitem__(self, item):
        return self.conf.get(item)

    def __len__(self):
        return len(self.conf)

    def get(self, opts, default=None, cast=None):
        if '.' not in opts:

            if cast is not None:
                return {k: cast(val) for k, val in self.conf[opts].items()}
            else:
                return self.conf[opts]

        main, opt = opts.split('.')

        if main not in self.conf:
            return default

        val = self.conf[main].get(opt)

        if opt is None:
            if cast is bool:
                return False
            elif cast is float or cast is int:
                return 0

            return default

        if val is None:
            return default

        if cast is not None:
            return cast(val)
        return val


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


class Entity(object):
    def __init__(self, type):
        self.type = type

    def __call__(self, cls):
        class Wrapped(cls):
            T = self.type

        return Wrapped
