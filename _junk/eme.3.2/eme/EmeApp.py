import json
import linecache
import os
from importlib import import_module
from os import listdir
from os.path import splitext

import sys

import logging

from vendor.eme.EntityPatch import EntityPatch
from abc import ABCMeta, abstractmethod


class EmeApp():

    def __init__(self):
        self.handlers = {}

    def send(self, client, rws):
        pass

    def getUser(self, client, rws):
        return None

    def loadHandlers(self, dirType, prefix="app"):
        cL = len(dirType)
        handlers = [splitext(f)[0] for f in sorted(listdir(prefix + "/" + dirType.lower()+"s")) if splitext(f)[0][-cL:] == dirType]

        for moduleName in handlers:
            module = import_module(prefix+"."+dirType.lower()+"s." + moduleName)
            handlerClass = getattr(module, moduleName)
            handler = handlerClass(self)
            self.handlers[moduleName[:-cL]] = handler

    def forgeAction(self, group, method):
        groups = group.split('/')
        group = groups.pop(0)
        if len(groups) > 0:
            method = method + '_' + '_'.join(groups)

        action = getattr(self.handlers[group], method)
        return action

    def parseEntity(self, entityDict):
        for key in entityDict:
            if isinstance(entityDict[key], dict):
                entityDict[key] = EntityPatch(entityDict[key])

        return EntityPatch(entityDict)

    def onMessageReceived(self, client, rws):
        group, method = rws["route"].split(":")

        try:
            user = self.getUser(client, rws)
            if not user:
                return

            action = self.forgeAction(group, method)
            if "params" in rws:
                if isinstance(rws["params"], list):
                    response = action([EntityPatch(a) for a in rws["params"]], user)
                else:
                    response = action(EntityPatch(rws["params"]), user)
            else:
                response = action(user)

            # automatic sending of response message (HTTP-like response for request)
            if isinstance(response, dict):
                self.send(client, response)
            elif isinstance(response, list):
                for resp in response:
                    self.send(client, resp)

        except Exception as e:
            print(e)
            logging.exception("MAIN")
            rws["error"] = "RWS parse: " + str(e)
            # self.send(client, rws)
            raise e

    # to be used for HTTP requests
    def parseRequest(self, rws):
        user = self.getUser(rws)

        if not user:
            logging.info("not user")
            pass

        try:
            arguments = self.parseRWSPayload(rws)
            arguments.append(user)

            return arguments
        except Exception as e:
            logging.exception("PARSEREQUEST")
            rws["error"] = "RWS parse: " + str(e)
            # self.send(client, rws)
            raise e

    def addRouting(self, index):
        verbs = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
        
        print('{0: <27}{1: <20}      {2}'.format('Route', 'Endpoint', 'Method'))
        for controllerName, controller in self.handlers.items():
            for methodName in dir(controller):
                if methodName.startswith("__") or methodName in ["rws", "server"] or not callable(getattr(controller, methodName)):
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
                    route = "/"+controllerName.lower()
                else:
                    route = "/"+controllerName.lower()+"/"+actionName
                endPoint = option.lower()+'_'+route[1:]
                if endPoint[-1] == '_':
                    endPoint += 'index'

                print('{0: <7}{1: <20}{2: <20} >    {3}'.format(option, route, endPoint, controllerName+"."+methodName))
                self.add_url_rule(route, endPoint, getattr(controller, methodName), methods=[option])
