import zipfile
from os.path import join


class BundleCommand:
    def __init__(self, cli):
        self.dbase = cli.script_path

    def run(self, auth: bool = True, cli: bool = True, tests: bool = True, frontend: bool = True, core: bool = True):

        prefix = 'noauth_' if not auth else ''

        with zipfile.ZipFile(join(self.dbase, 'content', prefix+'webapp.zip'), 'r') as zip_ref:
            zip_ref.extractall()

        if cli:
            with zipfile.ZipFile(join(self.dbase, 'content', prefix+'cli.zip'), 'r') as zip_ref:
                zip_ref.extractall()

        if tests:
            with zipfile.ZipFile(join(self.dbase, 'content', prefix+'tests.zip'), 'r') as zip_ref:
                zip_ref.extractall()

        if core:
            with zipfile.ZipFile(join(self.dbase, 'content', prefix+'core.zip'), 'r') as zip_ref:
                zip_ref.extractall()

        if not frontend:
            print("  -- Frontend-free bundle is not supported in this version!")

        print("Webapp + bundle created")
