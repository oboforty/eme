_modules = {}


class Module(object):
    def __init__(self, register=True):
        self.register = register

    def __call__(self, cls):
        class Wrapped(cls):
            pass

        if self.register:
            register_module(cls.__name__, cls)

        return Wrapped


def register_module(module_name, module_class):
    _modules[module_name] = module_class()


def init_webmodules(app, conf):
    for module in _modules.values():
        module.load_dal()
        module.load_webapp(app, conf)

        if hasattr(module, 'blueprint') and module.blueprint:
            app.register_blueprint(module.blueprint, module.blueprint_route)
        elif hasattr(module, 'blueprints') and module.blueprints:
            for blueprint_route, blueprint in module.blueprints.items():
                app.register_blueprint(blueprint, blueprint_route)


def init_climodules(app, conf):
    for module in _modules.values():
        module.load_dal()
        module.load_cliapp(app, conf)

        if hasattr(module, 'commands'):
            app.commands.extend(module.commands)


def init_wsmodules(app, conf):
    for module in _modules.values():
        module.load_dal()
        module.load_wsapp(app, conf)

        if hasattr(module, 'groups'):
            app.groups.extend(module.groups)
