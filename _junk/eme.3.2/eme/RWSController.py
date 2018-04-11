from vendor.eme.EntityPatch import EntityPatch


class RWSController():

    def rws(self, route, params, group=None):
        if hasattr(self, 'group'):
            route = self.group + ':' + route

        if isinstance(params, EntityPatch):
            params = dict(params)
        elif isinstance(params, list):
            params = [dict(e) for e in params]

        rws = {
            "route": route,
            "params": params
        }

        return rws