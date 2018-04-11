from vendor.eme.EntityPatch import EntityPatch
from vendor.eme.Singleton import Singleton
from vendor.eme.file import loadContent


class EntityManager(metaclass=Singleton):
    publicProperties = []
    rules = {}

    def __init__(self, entityType=None):
        if entityType is not None:
            self.rules = loadContent(entityType)

    def mapRules(self, entityPatch):
        entityPatch2 = EntityPatch(entityPatch.entityDict)
        entityPatch2.merge(self.rules[int(entityPatch.catId)])
        return entityPatch2

    def getRules(self, catId):
        return EntityPatch(self.rules[catId])
