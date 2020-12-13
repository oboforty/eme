import sys
from os.path import dirname, realpath, join

from eme.cli import CommandLineInterface
from eme.entities import load_settings


class ToolsCommandLineInterface(CommandLineInterface):

    def __init__(self):
        self.script_path = dirname(realpath(__file__))
        conf = load_settings(join(self.script_path, 'config.ini'))

        super().__init__(conf, self.script_path)


def main():
    app = ToolsCommandLineInterface()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
