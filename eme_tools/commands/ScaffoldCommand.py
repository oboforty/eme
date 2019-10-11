
class ScaffoldCommand:

    def __init__(self, cli):
        self.commands = {
            'scaffold:entity': {
                'help': 'Creates an empty webapp. Levels: Controller, Group, Task, Test, Entity, ',
                'short': {'l', 'levels='},
                'long': ['levels=']
            }
        }
