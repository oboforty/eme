from json import dumps

class RHTTPController():
    def rws(self, entity=None, entities=None, params=None, id=None, error=None):
        rws = {}

        if error:
            rws["error"] = error
        if id:
            rws["id"] = id

        if params:
            rws["params"] = params
        elif entity:
            rws["entity"] = entity.toDict()
        elif entities and len(entities) > 0:
            rws["entities"] = [entity.toDict() for entity in entities]

        return dumps(rws)