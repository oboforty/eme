import os
import shutil
import zipfile


class ForgeCommand:

    def __init__(self, cli):
        self.commands = {
            'forge:webapp': {
                'help': 'Creates an empty webapp',
                'short': {},
                'long': ['path=']
            }
        }

    def runWebapp(self, path: str):
        zip_path = 'eme_tools/packs/webapp.zip'

        if not os.path.exists(path):
            os.mkdir(path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(path)

        print("Webapp created in {}".format(path))

    def runTestapp(self, name: str):
        print("Testapp created in {}".format(name))

    def runWebsocketapp(self, name: str):
        print("Websocketapp created in {}".format(name))

    def runCore(self, name: str):
        print("Core created in {}".format(name))

    def runCliapp(self, name: str):
        print("Cliapp created in {}".format(name))

    def runTasks(self, name: str):
        print("Tasks created in {}".format(name))
