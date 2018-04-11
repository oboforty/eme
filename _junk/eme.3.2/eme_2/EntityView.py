from rom import Model

from vendor.eme.EntityPatch import EntityPatch


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
            if objName == 'entity' or isinstance(obj, Model) or isinstance(obj, EntityPatch) or obj is None:
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

        return _dict
