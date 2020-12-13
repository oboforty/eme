

class HelloCommand:
    """
    This is an example command
    """
    def __init__(self, cli):
        self.cli = cli

    def run(self, text: str = 'world'):
        print("Hello " + text)
