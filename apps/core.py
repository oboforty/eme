from importlib import import_module
from os import listdir
from os.path import splitext


def loadHandlers(ctx, dirType, prefix="apps"):
    cL = len(dirType)
    handlerNames = [splitext(f)[0] for f in sorted(listdir(prefix + "/" + dirType.lower() + "s")) if
                splitext(f)[0][-cL:] == dirType]
    handlers = {}

    for moduleName in handlerNames:
        module = import_module(prefix.replace('/', '.') + "." + dirType.lower() + "s." + moduleName)
        handlerClass = getattr(module, moduleName)
        handler = handlerClass(ctx)
        handlers[moduleName[:-cL]] = handler

    return handlers
