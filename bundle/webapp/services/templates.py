import json

from eme.entities import EntityJSONEncoder




def init(app, conf):

    @app.template_filter()
    def ejson(text):
        """Converts variable to json string using eme's extended encoder."""

        return json.dumps(text, cls=EntityJSONEncoder)
