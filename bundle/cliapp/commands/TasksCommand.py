from cliapp.scheduler import Scheduler


class TasksCommand():
    def __init__(self, server):
        self.server = server
        self.scheduler = None

        self.commands = {
            'tasks': {
                'help': 'Runs all tasks',
                'short': {},
                'long': ['tasks=']
            },
        }

    def getSch(self):
        if not self.scheduler:
            self.scheduler = Scheduler()

        return self.scheduler

    def run(self, tasks=None):
        sch = self.getSch()

        if tasks:
            sch.run(tasks.split(','))
        else:
            sch.run()
