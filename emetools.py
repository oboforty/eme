import sys

from eme_tools.cli import ToolsCommandLineInterface

# same as if you were executing simple_website/webapp/website.py
# with working directory: simple_website
app = ToolsCommandLineInterface()

if len(sys.argv) > 1:
    app.run(sys.argv)
else:
    app.start()
