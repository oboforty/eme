
class EntityCommand:

    def __init__(self, cli):
        pass

    def run(self, a: int, b: str = None, c = None):
        print("entity run", a, b, c)
