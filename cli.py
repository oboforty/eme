import sys
from commands.cli import CommandLineInterface


app = CommandLineInterface()

if len(sys.argv) > 1:
    app.run(sys.argv[1], sys.argv[2:] if len(sys.argv) > 2 else [])
else:
    while True:
        print("$geo~:", end="")
        cmd = input()
        if not cmd:
            break
        args = cmd.split(' ')
        app.run(args[0], args[1:] if len(args) > 1 else [])
