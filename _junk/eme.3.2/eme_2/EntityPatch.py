from decimal import Decimal
import json

_attrs =  ['items', 'values', 'keys']

class EntityPatch():
    def __init__(self, entityDict=None):
        if isinstance(entityDict, EntityPatch):
            entityDict = entityDict.entityDict
        if entityDict is None:
            entityDict = {}
        self.entityDict = dict(entityDict)
    
    def __getitem__(self, key):
        return self.entityDict[key]

    def __setitem__(self, key, value):
        self.entityDict[key] = value

    def __delitem__(self, key):
        del self.entityDict[key]

    def __getattr__(self, key):
        if key in _attrs:
            return getattr(self.entityDict, key)
        else:
            if key in self.entityDict:
                return self.entityDict[key]
            else:
                return None

    def __setattr__(self, key, value):
        if key != "entityDict":
            self.entityDict[key] = value
        else:
            return super().__setattr__(key, value)

    def __delattr__(self, key):
        if key in self.entityDict:
            del self.entityDict[key]
        elif hasattr(self, key):
            return super().__delattr__(key)

    def __iter__(self):
        return self.entityDict.__iter__()

    def __contains__(self, item):
        return self.entityDict.__contains__(item)

    def __hash__(self):
        return hash(json.dumps(self.entityDict))

    def __dict__(self):
        for objName, obj in self.entityDict.items():
            if isinstance(obj, Decimal):
                self.entityDict[objName] = float(obj)
        return self.entityDict

    def update(self, objDict):
        if isinstance(objDict, EntityPatch):
            self.entityDict.update(objDict.entityDict)
        else:
            self.entityDict.update(objDict)

    def copy(self):
        return EntityPatch(self.entityDict.copy())

    def apply(self, obj):
        if callable(obj):
            obj = obj()

        for attribute, value in self.entityDict.items():
            if attribute == "id":
                continue
            if isinstance(value, str):
                value = value.encode()
            setattr(obj, attribute, value)

        return obj
