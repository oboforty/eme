import json
import logging
from flask import Flask

from apps.core import loadHandlers


class Website(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='$[',
        variable_end_string=']$',
        comment_start_string='$#',
        comment_end_string='#$',
    ))

    def __init__(self, environment):
        conf = json.load(open('apps/website/config/{}.json'.format(environment)))

        super().__init__('/', static_url_path='', static_folder='apps/website/public', template_folder='apps/website/templates')

        self.handlers = loadHandlers(self, "Controller", prefix="apps/website")
        self.addRouting(index=conf['index'])

        logging.basicConfig(filename=conf['log_path'], level=logging.WARNING)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logger = logging.getLogger('ZWS')
        logger.addHandler(formatter)

        @self.after_request
        def after_request(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            #response.headers['Content-Type'] = 'application/json'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT,PATCH"
            #response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'

            return response

        self.host = conf['host']
        self.port = conf['port'] if 'port' in conf else 80

    def addRouting(self, index):
        verbs = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

        print('{0: <27}{1: <20}      {2}'.format('Route', 'Endpoint', 'Method'))
        for controllerName, controller in self.handlers.items():
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

                print('{0: <7}{1: <20}{2: <20} >    {3}'.format(option, route, endPoint,
                                                                controllerName + "." + methodName))
                self.add_url_rule(route, endPoint, getattr(controller, methodName), methods=[option])

    def start(self):
        self.run(self.host, self.port, threaded=True)

