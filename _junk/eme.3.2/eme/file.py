import json
from .EntityPatch import EntityPatch

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

def loadConfig(content):
    with open("app/content/" + content + ".json", encoding="utf8") as fh:
        return json.load(fh)
