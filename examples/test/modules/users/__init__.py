from eme.entities import load_handlers
from eme.modules import Module



# todo: eme BluePrint here
    # todo: discover controllers and make load_controllers work
    # self.controllers = load...


@Module
class UsersModule:
    def __init__(self):
        pass

    def load_webapp(self):
        self.blueprint = None
        self.blueprint_route = "users"

    def load_cliapp(self):
        # todo: discover these through modules into CLIApp and inject into (eme modules file)
        self.commands = load_handlers()

    def load_wsapp(self):
        pass

    def load_dal(self):
        # Todo: discover these through modules from migration (eme_utils module)
        self.entities = [

        ]

        self.repositories = [

        ]
