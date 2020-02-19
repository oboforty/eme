from os.path import realpath, dirname, join
from eme.entities import load_settings
from eme.website import WebsiteApp


from .services import templates, startup, mail, auth


class ExampleWebsite(WebsiteApp):

    def __init__(self):
        # eme/examples/simple_website is the working directory.
        script_path = dirname(realpath(__file__))
        conf = load_settings(join(script_path, 'config.ini'))

        super().__init__(conf, script_path)

        startup.init(self)
        templates.init(self, None)
        auth.init(self, conf['auth'])
        mail.init_mail(self, conf['mail'])


if __name__ == "__main__":
    app = ExampleWebsite()
    app.start()
