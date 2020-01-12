import logging
import sys
import argparse
import inspect
from os.path import join

from eme.entities import load_handlers


class CommandLineInterface():

    def __init__(self, conf, fbase='cliapp/'):
        # if len(config) == 0:
        #     raise Exception("Empty config file provided")
        self.conf = conf

        self.prefix = "$eme~:"
        sys.path.append(fbase)

        cdir = join(fbase, self.conf.get('cli.commands_dir', default='commands'))
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
        parser = argparse.ArgumentParser(argv)

        if hasattr(cmd, 'add_arguments'):
            # let the user handle the cmd arguments:
            getattr(cmd, 'add_arguments')(parser)
        else:
            # default parameters are determined from method signature:
            sig = inspect.signature(getattr(cmd, method_name))

            for par_name, pee in sig.parameters.items():
                kwargs = {}
                argument = par_name

                if pee.default != inspect._empty:
                    kwargs['default'] = pee.default

                if pee.annotation != inspect._empty:
                    if pee.annotation is bool:
                        argument = '--'+par_name

                        if 'default' in kwargs:
                            kwargs['required'] = False

                    elif pee.annotation is list:
                        kwargs['nargs'] = '+'
                    else:
                        kwargs['type'] = pee.annotation

                parser.add_argument(argument, **kwargs)

        # finally call the method using args
        method = getattr(cmd, method_name)

        if argv:
            # call method with arguments parsed with argparse
            args = parser.parse_args(argv)
            method(**vars(args))
        else:
            # no command arguments
            method()

    def run(self, argv=None):
        if argv is None:
            argv = sys.argv
        argv = argv.copy()

        _script = argv.pop(0)
        cmd_name = argv.pop(0)

        self.run_command(cmd_name, argv)

    def run_tasks(self, tasks=None):
        # todo: use absolute path!
        handler_tasks = load_handlers(self, 'Task')

        # Logging
        logger = logging.getLogger('geosch')
        logger.setLevel(logging.DEBUG)

        # file log
        fh = logging.FileHandler(self.conf.get('logfile', 'logs.txt'))
        lvl = self.conf.get('loglevel', 'WARNING')
        fh.setLevel(getattr(logging, lvl))

        # console log
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

        self.logger = logger
        self.debug_log = self.conf.get('scheduler.log_deep', False)


        if tasks is None:
            # all tasks
            tasks = handler_tasks.keys()

        for name in tasks:
            handler_tasks[name].run()
