import sys
import argparse
import inspect
from os.path import join

from eme.entities import load_handlers


class CommandLineInterface():

    def __init__(self, conf, fbase='cliapp/'):
        # if len(config) == 0:
        #     raise Exception("Empty config file provided")

        self.prefix = "$eme~:"

        cdir = join(fbase, conf.get('cli.commands_dir', default='commands'))
        self.commands = load_handlers(self, 'Command', cdir)

    def run_command(self, cmd_name, argv=None):
        if ':' in cmd_name:
            # subcommand
            cmd, subcmd = cmd_name.split(':')

            cmd_name = cmd.title()
            method_name = 'run_'+subcmd
        else:
            # main command
            cmd_name = cmd_name.title()
            method_name = 'run'

        cmd = self.commands[cmd_name]
        parser = argparse.ArgumentParser()

        if hasattr(cmd, 'add_arguments'):
            # let the user handle the cmd arguments:
            getattr(cmd, 'add_arguments')(parser)
        else:
            # default parameters are determined from method signature:
            sig = inspect.signature(getattr(cmd, method_name))

            for par_name, pee in sig.parameters.items():
                # if pee.default == inspect._empty:
                #     parser.add_argument('yeaa', type=int, nargs='+')
                #
                #     parser.add_argument('--arg1', nargs='+')
                # else:
                #     pass

                if pee.annotation == inspect._empty:
                    parser.add_argument(par_name)
                elif pee.annotation is bool:
                    parser.add_argument('--'+par_name)
                elif pee.annotation is list:
                    parser.add_argument(par_name, nargs='+')
                else:
                    parser.add_argument(par_name, type=pee.annotation)

        args = parser.parse_args(argv)

        # finally call the method using args
        method = getattr(cmd, method_name)
        method(**vars(args))

    def run(self, argv=None):
        if argv is None:
            argv = sys.argv

        _script = argv.pop(0)
        cmd_name = argv.pop(0)

        self.run_command(cmd_name, argv)



# def run(self, argv=None):
    #     """
    #     Reads and parses commands, mapping them to eme Command Handlers
    #
    #     """
    #     if argv is None:
    #         argv = sys.argv
    #
    #     if len(argv) < 2:
    #         print(self.help())
    #         return
    #
    #     cmd_full, opt_list = argv[1], argv[2:]
    #
    #     if ':' in cmd_full:
    #         cmd_name, cmd_sub = cmd_full.split(':')
    #         scmd = 'run' + cmd_sub.title()
    #
    #         if cmd_name.title() not in self.commands or not hasattr(self.commands[cmd_name.title()], scmd):
    #            print('Command not found')
    #            return
    #
    #         obj = self.commands[cmd_name.title()]
    #         cmd = getattr(obj, scmd)
    #
    #     else:
    #         if cmd_full.title() not in self.commands:
    #            print('Command not found')
    #            return
    #
    #         cmd_sub = cmd_full
    #         obj = self.commands[cmd_full.title()]
    #         cmd = obj.run
    #
    #     short, long = self.buildCommandList(obj, cmd_full)
    #
    #     try:
    #         opts, args = getopt.getopt(opt_list, short, long)
    #     except getopt.GetoptError as e:
    #         print(self.help())
    #         return
    #
    #     params = {}
    #
    #     for opt, arg in opts:
    #         # convert single letter to fuller equivalent
    #         if opt[:2] == '--':
    #             opt = opt[2:]
    #         else:
    #             ff = opt[1:]
    #             opt = obj.commands[cmd_full]['short'][ff][:-1]
    #
    #         if opt == 'help':
    #             print(obj.commands[cmd_full].get(cmd_sub, 'No help available for this command'))
    #             return
    #         else:
    #             params[opt] = arg
    #
    #     #try:
    #     cmd(**params)
    #     #except Exception as e:
    #     #    raise e
    #
    # def buildCommandList(self, obj, cmd_name):
    #
    #     cmd_obj = obj.commands[cmd_name]
    #     short = ''
    #
    #     for sh, ln in cmd_obj['short'].items():
    #         short += sh
    #
    #         if ln[-1] == '=':
    #             short += ':'
    #
    #     long = cmd_obj['long']
    #
    #     return short, long
    #
    # def start(self):
    #     """
    #     Starts CLI app, accepting multiple commands
    #     """
    #
    #     while True:
    #         self.help()
    #
    #         print(self.prefix, end="")
    #         cmd = input()
    #         if cmd == 'exit' or cmd == 'quit':
    #             break
    #
    #         self.run(['a'] + cmd.split(' '))
    #
    # def help(self):
    #
    #     return "todo help"
