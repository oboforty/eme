import os
from eme.entities import load_handlers, load_settings
from eme.modules import Module

from .services.jinja_helpers import init_jinja
from .services.mail import init_mail


@Module
class UtilsModule:
    def __init__(self):
        self.module_path = os.path.dirname(os.path.realpath(__file__))
        self.conf = load_settings(os.path.join(self.module_path, 'config.ini'))
        self.commands = []

    def load_webapp(self, app, conf):
        init_jinja(app, conf)

        init_mail(app, self.conf['mail'])

    def load_cliapp(self, app, conf):
        self.commands = load_handlers(self, 'Command', 'commands', self.module_path)

    def load_wsapp(self, app, conf):
        pass

    def load_dal(self):
        pass
