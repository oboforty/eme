import inspect
import logging
import sys
from collections import defaultdict
from os.path import join

from flask import Flask, Blueprint
from werkzeug.routing import BaseConverter

from .entities import load_handlers


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

CTRL_ATTRIBUTES = ['server', 'app']


from flask import request

class WebsiteAppBase:

    def __init__(self, config: dict, path='webapp'):
        if len(config) == 0:
            raise Exception("Empty config file provided")
        webconf = config.get('website', {})

        # Routing
        self._custom_routes = defaultdict(set)
        self.module_route = ""

        # Socket
        self.host = webconf.get('host', '0.0.0.0')
        self.port = webconf.get('port')

        # Flags
        self.debug = webconf.get('debug', False)
        #self.testing = webconf.get('testing')
        self.develop = webconf.get('develop', False)

        self.http_verbs = webconf.get('methods', ["GET","HEAD","OPTIONS","POST","PUT","PATCH","DELETE"])

        web_type = webconf.get('type', 'webapp')
        headers = config.get('headers', {
            "Access-Control-Allow-Methods":  ",".join(self.http_verbs),
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type"
        })

        if web_type == 'webapp':
            # Load default controllers
            self.load_controllers(load_handlers(self, 'Controller', path=join(path, 'controllers')), conf=config.get('routing', {}))
        elif web_type == 'webapi':
            # Load default controllers
            self.load_controllers(load_handlers(self, 'Api', module_path='api', path=join(path, 'api')), conf=config.get('routing', {}))

            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/json'
                headers['Referrer-Policy'] = 'no-referrer-when-downgrade'

        # if self.develop:
        #     @self.after_request
        #     def after_request(response):
        #         # in debug mode we also server static files, hence the lack of forcing
        #         h = headers.copy()
        #         if response.mimetype not in ('text/html', ):
        #             del h['Content-Type']
        #
        #         response.headers.update(h)
        #         return response
        # else:
        @self.after_request
        def after_request(response):
            response.headers.update(headers)
            return response



    def get_paths(self, config: dict, path='webapp'):
        webconf = config.get('website', {})

        template_folder = join(path, webconf.get('template_folder', 'templates'))
        static_url = webconf.get('static_url_path', '')
        static_folder = join(path, webconf.get('static_folder', 'public'))

        return template_folder,static_folder,static_url

    def preset_endpoint(self, new_url, endpoint):
        # strip the verb from the url
        sp = new_url.split(' ')
        prefix = 'GET' if len(sp) == 1 else sp[0].upper()
        new_url = ''.join(sp[1:])

        # force the GET keyword into the endpoint
        controller, method = endpoint.split(':')
        if prefix == 'GET' and method[0:3].lower() != 'get':
            method = prefix.lower() + '_' + method

        # custom routes are a map of {Controller.verb_method -> overridden_url}
        self._custom_routes[controller + ':' + method].add(new_url)

    def preset_endpoints(self, rules):
        for new_url, endpoint in rules.items():
            self.preset_endpoint(new_url, endpoint)

    def load_controllers(self, controllers: dict, conf=None):
        debug_len = conf.get('__debug_len__', 20)
        index = conf.get('__index__')

        print(('{0: <7}{1: <'+str(debug_len)+'}{2}').format("OPT", "ROUTE", "ENDPOINT"))

        for controller_name, controller in controllers.items():
            if not hasattr(controller, 'group'):
                controller.group = controller_name
            if not hasattr(controller, 'route'):
                controller.route = controller.group.lower()

            for method_name in dir(controller):
                method = getattr(controller, method_name)

                if method_name.startswith("__") or not callable(method):
                    continue
                if method_name in CTRL_ATTRIBUTES:
                    continue

                option = "GET"
                action_name = method_name
                methods = method_name.split('_')

                if methods[0].upper() in self.http_verbs:
                    option = methods.pop(0).upper()
                    action_name = '_'.join(methods)

                # define endpoint (used in eme//flask internally)
                endpoint = controller.group + ':' + option.lower() + '_' + action_name
                if endpoint[-1] == '_':
                    endpoint = endpoint[:-1]
                    #endpoint += 'index'

                # check if a custom routing rule has overridden the default one
                if endpoint in self._custom_routes:
                    routes = self._custom_routes[endpoint]
                else:
                    # otherwise eme automatically guesses the route
                    if index == endpoint:
                        # default route without action is index
                        route = "/"
                        # todo: index controller other actions?
                    elif method_name == "index" or action_name == "":
                        route = "/" + controller.route
                    else:
                        route = "/" + controller.route + "/" + action_name

                    # modify route with url's input params:
                    sig = inspect.signature(method)
                    for par_name, par in sig.parameters.items():
                        if par_name in ['args', 'kwargs']:
                            continue

                        if par.annotation != inspect._empty and par.annotation is not str:
                            inp = f'/<{par.annotation.__name__}:{par_name}>'
                        else:
                            inp = f'/<{par_name}>'

                        route += inp

                    # fake set:
                    routes = {route}

                # todo: stop reconfiguring the same route, not endpoint!
                # if endpoint in self.view_functions:
                #     # if endpoint is already configured, we ignore
                #     continue

                for route in routes:
                    print(('{0: <7}{1: <'+str(debug_len)+'}{2}').format(option, route, self.module_route+endpoint))
                    self.add_url_rule(route, endpoint, getattr(controller, method_name), methods=[option])

    def init_modules(self, modules, webconf):
        for module in modules:
            module.init_dal()
            module.init_webapp(self, webconf)

            if hasattr(module, 'blueprint') and module.blueprint:
                self.register_blueprint(module.blueprint, url_prefix=module.blueprint.module_route)
            elif hasattr(module, 'blueprints') and module.blueprints:
                for blueprint in module.blueprints:
                    self.register_blueprint(blueprint, url_prefix=blueprint.module_route)


class WebsiteApp(Flask, WebsiteAppBase):

    def __init__(self, config: dict, path: str):
        sys.path.append(path)

        template_folder, static_folder, static_url = self.get_paths(config,path)
        Flask.__init__(self, '/', static_url_path=static_url, static_folder=static_folder, template_folder=template_folder)
        self.url_map.converters['regex'] = RegexConverter
        WebsiteAppBase.__init__(self, config, path=path)

    def start(self):
        self.run(self.host, self.port, threaded=True, debug=self.debug)


class WebsiteBlueprint(Blueprint, WebsiteAppBase):

    def __init__(self, name, config: dict, path: str, module_route=""):
        self.module_route = module_route

        template_folder, static_folder, static_url = self.get_paths(config, path)
        Blueprint.__init__(self, name, name, static_url_path=static_url, static_folder=static_folder, template_folder=template_folder)
        WebsiteAppBase.__init__(self, config, path=path)
