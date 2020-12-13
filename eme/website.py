import inspect
import logging
import sys
from collections import defaultdict
from os.path import join

from flask import Flask, Blueprint
from werkzeug.routing import BaseConverter

from .entities import load_handlers
from .modules import init_webmodules


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

CTRL_ATTRIBUTES = ['server', 'app']


class WebsiteAppBase:

    def __init__(self, config: dict, fbase='webapp'):
        if len(config) == 0:
            raise Exception("Empty config file provided")
        webconf = config['website']

        # Routing
        self._custom_routes = defaultdict(set)
        self.url_map.converters['regex'] = RegexConverter

        # Socket
        self.host = webconf.get('host', '0.0.0.0')
        self.port = webconf.get('port')

        # Flags
        self.debug = webconf.get('debug')
        #self.testing = webconf.get('testing')
        self.develop = webconf.get('develop')

        self.http_verbs = webconf.get('methods')

        web_type = webconf.get('type', 'webapp')
        headers = config.get('headers', {
            "Access-Control-Allow-Methods":  ",".join(self.http_verbs),
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type"
        })

        if web_type == 'webapp':
            # Load default controllers
            self.load_controllers('Controller', fbase, webconf.get('controllers_dir'), conf=config['routing'])
        elif web_type == 'webapi':
            # Load default controllers
            self.load_controllers('Api', fbase, webconf.get('api_dir'), conf=config['routing'])

            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/json'
                headers['Referrer-Policy'] = 'no-referrer-when-downgrade'

        @self.after_request
        def after_request(response):
            response.headers.update(headers)
            return response

    def get_paths(self, config: dict, fbase='webapp'):
        webconf = config['website']

        template_folder = join(fbase, webconf.get('template_folder', 'templates'))
        static_url = webconf.get('static_url_path', '')
        static_folder = join(fbase, webconf.get('static_folder', 'public'))

        return template_folder,static_folder,static_url

    def preset_endpoint(self, new_url, endpoint):
        # strip the verb from the url
        sp = new_url.split(' ')
        prefix = 'GET' if len(sp) == 1 else sp[0].upper()
        new_url = ''.join(sp[1:])

        # force the GET keyword into the endpoint
        controller, method = endpoint.split('.')
        if prefix == 'GET' and method[0:3].lower() != 'get':
            method = prefix.lower() + '_' + method

        # custom routes are a map of {Controller.verb_method -> overridden_url}
        self._custom_routes[controller + '.' + method].add(new_url)

    def preset_endpoints(self, rules):
        for new_url, endpoint in rules.items():
            self.preset_endpoint(new_url, endpoint)

    def load_controllers(self, class_name, fbase=None, path=None, conf=None):
        debug_len = conf.get('__debug_len__', 20)
        index = conf.get('__index__')

        print(('{0: <7}{1: <'+str(debug_len)+'}{2}').format("OPT", "ROUTE", "ENDPOINT"))

        # automatically parses custom
        controllers = load_handlers(self, class_name, path, prefix_path=fbase)

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
                endpoint = controller.group + '.' + option.lower() + '_' + action_name
                if endpoint[-1] == '_':
                    endpoint += 'index'

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
                    print(('{0: <7}{1: <'+str(debug_len)+'}{2}').format(option, route, endpoint))
                    self.add_url_rule(route, endpoint, getattr(controller, method_name), methods=[option])

                #self.view_functions
                #self.url_map


class WebsiteApp(Flask, WebsiteAppBase):

    def __init__(self, config: dict, fbase: str = 'webapp'):
        sys.path.append(fbase)

        template_folder, static_folder, static_url = self.get_paths(config,fbase)
        Flask.__init__(self, '/', static_url_path=static_url, static_folder=static_folder, template_folder=template_folder)
        WebsiteAppBase.__init__(self, config, fbase=fbase)

        init_webmodules(self, config)

    def start(self):
        self.run(self.host, self.port, threaded=True, debug=self.debug)


class WebsiteBlueprint(Blueprint, WebsiteAppBase):

    def __init__(self, config: dict, fbase: str):
        template_folder, static_folder, static_url = self.get_paths(config,fbase)
        Blueprint.__init__(self, '/', static_url_path=static_url, static_folder=static_folder, template_folder=template_folder)
        WebsiteAppBase.__init__(self, config, fbase=fbase)
