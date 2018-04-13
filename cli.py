import sys
from apps.cli.cli import cli

app = CommandLineInterface()

if __name__ == "__main__":
  if len(sys.argv) > 1:
    app.run(sys.argv[1], sys.argv[2:] if len(sys.argv) > 2 else [])
  else:
    while True:
      print("$geo:", end="")
      cmd = input()
      if not cmd:
        break
      args = cmd.split(' ')
      geo.run(args[0], args[1:] if len(sys.argv) > 1 else [])
