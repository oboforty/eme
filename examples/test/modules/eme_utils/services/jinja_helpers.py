
import json

from eme.entities import EntityJSONEncoder


def init_jinja(app, conf):

    @app.template_filter()
    def ejson(text):
        """Converts variable to json string using eme's extended encoder."""

        return json.dumps(text, cls=EntityJSONEncoder)

    @app.context_processor
    def utility_processor():
        def varval(entity, attr, sub=None):
            if entity is not None and hasattr(entity, attr):
                v = getattr(entity, attr)

                if sub is not None:
                    return v[sub]
                return v
            return ''

        return dict(varval=varval)
