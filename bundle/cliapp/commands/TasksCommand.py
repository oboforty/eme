

class TasksCommand:
    def __init__(self, cli):
        self.cli = cli

    def run(self, tasks: list = None):
        self.cli.run_tasks(tasks)
