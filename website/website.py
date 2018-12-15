import logging

from flask import Flask
from werkzeug.routing import BaseConverter

from core.ctx import config
from core.eme import loadHandlers, loadConfig


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class Website(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='{=',
        variable_end_string='=}',
        comment_start_string='{#',
        comment_end_string='#}',
    ))

    def __init__(self):
        dir = 'website/'

        conf = loadConfig(dir+'config.ini')['website']

        super().__init__('/', static_url_path='', static_folder=dir+'public', template_folder=dir+'templates')
        self.manualRoutes = {}
        self.ws_address = conf.get('ws_address')
        self.controllers = loadHandlers(self, "Controller", prefix=dir)
        self.host = conf.get('host')
        self.port = conf.get('port')

        self.url_map.converters['regex'] = RegexConverter

        self.addRouting(index=conf['index'])
        #self.json_encoder = EntityJSONEncoder

        logging.basicConfig(filename=dir+'logs.txt', level=logging.WARNING)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logger = logging.getLogger('ZWS')
        logger.addHandler(formatter)

        @self.after_request
        def after_request(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT,PATCH"

            #if hasattr(response, 'api') and response.api:
            #    response.headers['Content-Type'] = 'application/json'
            #response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'

            return response

    def setRouting(self, rules):
        self.manualRoutes.update(rules)

    def addRouting(self, index):
        verbs = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

        print('{0: <27}{1: <20}      {2}'.format('Route', 'Endpoint', 'Method'))
        for controllerName, controller in self.controllers.items():
            for methodName in dir(controller):
                if methodName.startswith("__") or methodName in ["rws", "server"] or not callable(
                        getattr(controller, methodName)):
                    continue
                option = "GET"
                actionName = methodName
                methods = methodName.split('_')

                if methods[0].upper() in verbs:
                    option = methods.pop(0).upper()
                    actionName = '_'.join(methods)

                if index == controllerName and methodName == "index":
                    route = "/"
                elif methodName == "index" or actionName == "":
                    route = "/" + controllerName.lower()
                else:
                    route = "/" + controllerName.lower() + "/" + actionName
                endPoint = option.lower() + '_' + route[1:]
                if endPoint[-1] == '_':
                    endPoint += 'index'

                if route in self.manualRoutes:
                    route = self.manualRoutes[route]
                print('{0: <7}{1: <20}{2: <20} >    {3}'.format(option, route, endPoint, controllerName + "." + methodName))
                self.add_url_rule(route, endPoint, getattr(controller, methodName), methods=[option])

    def start(self):
        self.run(self.host, self.port, threaded=True, debug=False)
