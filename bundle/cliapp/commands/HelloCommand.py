

class HelloCommand:
    """
    This is an example command, shows you how to use it
    """
    def __init__(self, cli):
        self.cli = cli

    def run(self, text: str = 'world'):
        print("Hello " + text)
