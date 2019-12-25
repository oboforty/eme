from os.path import realpath, dirname
from eme.entities import load_config
from eme.website import WebsiteApp


class ExampleWebsite(WebsiteApp):

    def __init__(self):
        # eme/examples/simple_website is the working directory.
        script_path = dirname(realpath(__file__))
        conf = load_config('webapp/config.ini')

        super().__init__(conf, script_path)


if __name__ == "__main__":
    app = ExampleWebsite()
    app.start()
