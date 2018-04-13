import sys

from apps.core import loadHandlers


class CommandLineInterface():

    def __init__(self):
        self.handlers = loadHandlers(self, "Command", prefix="apps/cli")

    def run(self, group, args):
        self.handlers[group.title()].run(*args)
