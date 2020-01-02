import sys
from os.path import dirname, realpath, join

from eme.cli import CommandLineInterface
from eme.entities import load_settings


class ToolsCommandLineInterface(CommandLineInterface):

    def __init__(self):
        script_path = dirname(realpath(__file__))
        conf = load_settings(join(script_path, 'config.ini'))

        super().__init__(conf, script_path)


def main():
    app = ToolsCommandLineInterface()

    if len(sys.argv) > 1:
        app.run(sys.argv)
    else:
        app.start()


if __name__ == '__main__':
    main()
