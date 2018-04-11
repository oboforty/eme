import json

_content = {}

def loadContent(content, patch=True, keep=True):
    if content not in _content:
        with open("bll/content/" + content + ".json", encoding="utf8") as fh:
            js = json.load(fh)
            if not patch or isinstance(js, list):
                _content[content] = js
            else:
                _content[content] = EntityPatch(js)

    return _content[content]

def unloadContent(content):
    if content in _content:
        del _content[content]


class EntityPatch():
    def __init__(self, content, **kwargs):
        if not content:
            self.__dict__ = kwargs
        elif isinstance(content, dict):
            self.__dict__ = content
        else:
            self.__dict__ = content.__dict__

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