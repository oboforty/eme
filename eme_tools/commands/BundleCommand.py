import zipfile
import os


class BundleCommand:
    def __init__(self, cli):
        self.dbase = cli.script_path

    def run(self, name: str, auth: bool = True, cli: bool = True, examples: bool = True, websocket: bool = True, frontend: bool = True, core: bool = True, postgres: bool = False, mysql: bool = False, oracle: bool = False):
        if os.path.exists(name):
            raise Exception("Project already exists: {}!".format(name))

        os.mkdir(name)
        prefix = 'noauth_' if not auth else ''

        with zipfile.ZipFile(os.path.join(self.dbase, 'content', prefix+'webapp.zip'), 'r') as zip_ref:
            zip_ref.extractall(name)

        if not examples:
            # delete examples from other webapp
            os.remove(os.path.join(name, 'webapp', 'controllers', 'ExamplesController.py'))

        if cli:
            with zipfile.ZipFile(os.path.join(self.dbase, 'content', prefix+'cliapp.zip'), 'r') as zip_ref:
                zip_ref.extractall(name)

            if not examples:
                # delete examples from other cli
                os.remove(os.path.join(name, 'cliapp', 'commands', 'HelloCommand.py'))

        if websocket:
            with zipfile.ZipFile(os.path.join(self.dbase, 'content', prefix+'ws.zip'), 'r') as zip_ref:
                zip_ref.extractall(name)

            if not examples:
                # delete examples from other cli
                os.remove(os.path.join(name, 'wsapp', 'groups', 'ExampleGroup.py'))

        if examples:
            with zipfile.ZipFile(os.path.join(self.dbase, 'content', prefix+'testapp.zip'), 'r') as zip_ref:
                zip_ref.extractall(name)

        if core:
            with zipfile.ZipFile(os.path.join(self.dbase, 'content', prefix+'core.zip'), 'r') as zip_ref:
                zip_ref.extractall(name)

            # write ctx
            b = os.path.join(name, 'core', 'content', 'ctx.ini')
            with open(b, 'r') as fh:
                ctx_tpl = fh.read()
            with open(b, 'w') as fh:
                db = 'postgres' if postgres else ('mysql' if mysql else ('oracle' if oracle else 'sqlite'))
                fh.write(ctx_tpl.format(name, db))

        if not frontend:
            print("  -- Frontend-free bundle is not supported in this version!")

        print("Webapp + bundle created at " + name)
