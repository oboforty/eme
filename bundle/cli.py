import sys

from cliapp.cli import ExampleCommandLineInterface


def main():
    app = ExampleCommandLineInterface()

    if len(sys.argv) > 1:
        app.run(sys.argv)
    else:
        app.start()


if __name__ == '__main__':
    main()
