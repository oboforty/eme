import sys
import getopt

from eme.entities import loadHandlers


class CommandLineInterface():

    def __init__(self, directory='cliapp/'):
        self.prefix = "$eme~:"
        self.commands = loadHandlers(self, 'Command', prefix=directory)

    def run(self, argv):
        """
        Reads and parses commands, mapping them to eme Command Handlers

        """
        if len(argv) < 2:
            print(self.help())
            return

        cmd_full, opt_list = argv[1], argv[2:]

        if ':' in cmd_full:
            cmd_name, cmd_sub = cmd_full.split(':')
            scmd = 'run' + cmd_sub.title()

            if cmd_name.title() not in self.commands or not hasattr(self.commands[cmd_name.title()], scmd):
               print('Command not found')
               return

            obj = self.commands[cmd_name.title()]
            cmd = getattr(obj, scmd)

        else:
            if cmd_full.title() not in self.commands:
               print('Command not found')
               return

            cmd_sub = cmd_full
            obj = self.commands[cmd_full.title()]
            cmd = obj.run

        short, long = self.buildCommandList(obj, cmd_full)

        try:
            opts, args = getopt.getopt(opt_list, short, long)
        except getopt.GetoptError as e:
            print(self.help())
            return

        params = {}

        for opt, arg in opts:
            # convert single letter to fuller equivalent
            if opt[:2] == '--':
                opt = opt[2:]
            else:
                ff = opt[1:]
                opt = obj.commands[cmd_full]['short'][ff][:-1]

            if opt == 'help':
                print(obj.commands[cmd_full].get(cmd_sub, 'No help available for this command'))
                return
            else:
                params[opt] = arg

        #try:
        cmd(**params)
        #except Exception as e:
        #    raise e

    def buildCommandList(self, obj, cmd_name):

        cmd_obj = obj.commands[cmd_name]
        short = ''

        for sh, ln in cmd_obj['short'].items():
            short += sh

            if ln[-1] == '=':
                short += ':'

        long = cmd_obj['long']

        return short, long

    def start(self):
        """
        Starts CLI app, accepting multiple commands
        """

        while True:
            self.help()

            print(self.prefix, end="")
            cmd = input()
            if cmd == 'exit' or cmd == 'quit':
                break
            self.run(cmd)

        #return self.run(sys.argv)

    def help(self):

        return "todo help"


if __name__ == "__main__":

    app = CommandLineInterface()

    app.run(sys.argv)
