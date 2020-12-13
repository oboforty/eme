import zipfile
import os


class ModuleCommand:
    def __init__(self, cli):
        self.dbase = cli.script_path

    def run(self, name):
        if not os.path.exists('modules'):
            raise Exception("This is not an eme project! 'modules' directory does not exist.")

        path = os.path.join('modules', name)
        if os.path.exists(path):
            raise Exception(f"Module '{name}' already added to this project!")

        os.mkdir(path)

        with zipfile.ZipFile(os.path.join(self.dbase, 'modules', name+'.zip'), 'r') as zip_ref:
            zip_ref.extractall(path)

        # move files in __move__ directory to app bundle
        mopath = os.path.join('modules', name, '__move__')
        for top, dirs, files in os.walk(mopath):
            for file in files:
                rel_dir = os.path.relpath(top, mopath)
                rel_file = os.path.join(rel_dir, file)
                abs_file = os.path.join(top, file)

                if not os.path.exists(rel_dir):
                    os.makedirs(rel_dir)

                # file relative in __move__ directory is the relative path to the working directory
                if not os.path.exists(rel_file):
                    # eme module files are only added once!
                    os.rename(abs_file, rel_file)

        print(f"Module {name} added to project")
