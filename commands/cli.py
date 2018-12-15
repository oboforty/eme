from core.eme import loadHandlers


class CommandLineInterface:

    def __init__(self):
        self.commands = loadHandlers(self, "Command", prefix="commands")

    def run(self, group, args):
        cmd_name = group.title()

        if ':' in cmd_name:
            cmd_name, scmd = cmd_name.split(':')
            scmd = 'run' + scmd.title()

            if cmd_name not in self.commands or not hasattr(self.commands[cmd_name], scmd):
               print('Command not found')
               return

            cmd = getattr(self.commands[cmd_name], scmd)

        else:
            if cmd_name not in self.commands:
               print('Command not found')
               return
            cmd = self.commands[cmd_name].run

        try:
            cmd(*args)
        except Exception as e:
            raise e
