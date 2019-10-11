import logging
from collections import defaultdict

from flask import Flask
from werkzeug.routing import BaseConverter

from .entities import loadHandlers


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

http_verbs = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

class WebsiteApp(Flask):
    jinja_options = Flask.jinja_options.copy()
    #jinja_options.update()

    def __init__(self, config: dict):
        conf = config['website']
        crou = config['routing']
        chead = config['headers']

        super().__init__('/',
                         static_url_path=conf.get('static_url_path', ''),
                         static_folder=conf.get('static_folder', 'static'),
                         template_folder=conf.get('template_folder', 'templates'))

        # Controllers
        self.manualRoutes = {}
        self.urlRules = defaultdict(set)
        self.controllers = loadHandlers(self, "Controller", prefix=conf.get('controllers_folder'))

        # Socket
        self.host = conf.get('host')
        self.port = conf.get('port')

        # Flags
        self.debug = conf.get('debug') == 'yes'
        #self.testing = conf.get('testing') == 'yes'
        self.develop = conf.get('develop') == 'yes'

        self.url_map.converters['regex'] = RegexConverter
        #self.json_encoder = EntityJSONEncoder

        # Routing
        routes = crou.copy()
        index = routes.pop('index')
        self.urlRules.update(routes)
        self.addRouting(index=index)

        # Logging
        if not conf.get('debug'):
            logging.basicConfig(filename=conf.get('log_file'), level=logging.WARNING)
            formatter = logging.Formatter(conf.get('log_format', '%(asctime)s %(levelname)s %(message)s'))
            logger = logging.getLogger(conf.get('log_prefix', 'web'))
            logger.addHandler(formatter)

        @self.after_request
        def after_request(response):
            for name, val in chead.items():
                response.headers[name] = val

            #if hasattr(response, 'api') and response.api:
            #    response.headers['Content-Type'] = 'application/json'
            #response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'

            return response

    def setRouting(self, rules):
        self.manualRoutes.update(rules)

    def addUrlRule(self, rules):
        for new_url, endpoint in rules.items():
            sp = new_url.split(' ')
            prefix = 'GET' if len(sp) == 1 else sp[0].upper()

            new_url = ''.join(sp[1:])

            self.urlRules[prefix.lower() + '__' + endpoint].add(new_url)

    def addRouting(self, index):
        print('{0: <27}{1: <20}      {2}'.format('Route', 'Endpoint', 'Method'))
        for controllerName, controller in self.controllers.items():
            for methodName in dir(controller):
                if methodName.startswith("__") or methodName in ["rws", "server"] or not callable(
                        getattr(controller, methodName)):
                    continue
                option = "GET"
                actionName = methodName
                methods = methodName.split('_')

                if methods[0].upper() in http_verbs:
                    option = methods.pop(0).upper()
                    actionName = '_'.join(methods)

                # default route without action is index
                if index == controllerName and methodName == "index":
                    route = "/"
                elif methodName == "index" or actionName == "":
                    route = "/" + controllerName.lower()
                else:
                    route = "/" + controllerName.lower() + "/" + actionName
                endPoint = option.lower() + '__' + route[1:]
                if endPoint[-1] == '_':
                    endPoint += 'index'

                if endPoint in self.urlRules:
                    # Reroute url by endpoint
                    for route in self.urlRules[endPoint]:
                        print('{0: <7}{1: <20}{2: <20} >    {3}'.format(option, route, endPoint, controllerName + "." + methodName))
                        self.add_url_rule(route, endPoint, getattr(controller, methodName), methods=[option])
                else:
                    manroute = option.upper() + " " + route

                    if manroute in self.manualRoutes:
                        # Add manual root
                        route = self.manualRoutes[manroute]

                    # output and add routes
                    print('{0: <7}{1: <20}{2: <20} >    {3}'.format(option, route, endPoint, controllerName + "." + methodName))
                    self.add_url_rule(route, endPoint, getattr(controller, methodName), methods=[option])

    def start(self):
        self.run(self.host, self.port, threaded=True, debug=self.debug)
