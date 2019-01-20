import sys

from cliapp.cli import ExampleCommandLineInterface

# same as if you were executing simple_website/webapp/website.py
# with working directory: simple_website
app = ExampleCommandLineInterface()

if len(sys.argv) > 1:
    app.run(sys.argv)
else:
    app.start()
