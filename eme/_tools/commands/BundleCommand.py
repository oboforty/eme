import zipfile
import os
from collections import namedtuple

from eme._tools.commands.ModuleCommand import ModuleCommand


class BundleCommand:
    def __init__(self, cli):
        self.dbase = cli.script_path

    def run(self, name: str, complete: bool = True, auth: bool = True, websocket: bool = True, frontend: str = 'native', database: bool = True):
        if os.path.exists(name):
            raise Exception("Project already exists: {}!".format(name))

        os.mkdir(name)

        with zipfile.ZipFile(os.path.join(self.dbase, 'content', '_eme_bundle_complete.zip'), 'r') as zip_ref:
            zip_ref.extractall(name)

        os.chdir(name)
        os.mkdir('modules')
        mc = ModuleCommand(namedtuple('Cli', 'script_path')(self.dbase))

        if complete or auth:
            mc.run('eme_utils')
            mc.run('users')

        if frontend:
            mc.run('fe_boilerplate_bootstrap_'+frontend)

        print("Eme bundle created at " + name)
