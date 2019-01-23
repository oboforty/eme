import random


class ScrambleCommand:

    def __init__(self, cli):
        self.commands = {
            'scramble': {
                'help': 'scrambles an input sentence',
                'short': {'w': 'word='},
                'long': ['word=']
            }
        }

    def run(self, word: str):
        l = list(word)
        random.shuffle(l)
        newWord = ''.join(l)

        print("Original word: {}, Scrambled: {}".format(word, newWord))

