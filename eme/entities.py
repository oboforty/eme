import configparser
import os
import time
from datetime import datetime, date
from enum import Enum
from importlib import import_module
from json import JSONEncoder
from uuid import UUID

import inflect


def load_handlers(ctx, class_suffix, module_path=None, path=None):
    """
    Loads EME handlers
    :param ctx: parent app class instance
    :param class_suffix: handler class as suffix. loaded classes must have this suffix
    :param module_path: module_path from app/module handler root
    :param path: sys.path for the app/module. must be included in sys.app
    """

    # smart-guess: plural handler type
    if module_path is None:
        p = inflect.engine()
        module_path = p.plural_noun(class_suffix).lower()
        
    # replace / to . in module_path:
    if os.sep in module_path:
        module_path = module_path.replace(os.sep, '.')
    if '/' in module_path:
        module_path = module_path.replace('/', '.')
    module_path = module_path.lstrip('.').rstrip('.')

    # list handler names:
    handler_names = [os.path.splitext(f)[0] for f in sorted(os.listdir(path)) if f.endswith(class_suffix + '.py')]
    handlers = {}

    # load the modules:
    CL = -len(class_suffix) if class_suffix else None
    for module_name in handler_names:
        module = import_module(module_path + "." + module_name)

        # instantiate class
        handler_class = getattr(module, module_name)
        handler = handler_class(*ctx) if isinstance(ctx, tuple) else handler_class(ctx)
        handlers[module_name[:CL]] = handler

    return handlers


def load_config(file):
    config = configparser.ConfigParser()
    config.read(file)

    return config._sections


def load_settings(file):
    conf = load_config(file)

    if not conf:
        return None

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
                return self.conf.get(opts, default)

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

    @property
    def view(self):
        return self.conf.copy()


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
