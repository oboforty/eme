from os.path import realpath, dirname, join
from eme.entities import load_settings
from eme.website import WebsiteApp


from .services import filters, startup, login, mail


class ExampleWebsite(WebsiteApp):

    def __init__(self):
        # eme/examples/simple_website is the working directory.
        script_path = dirname(realpath(__file__))
        conf = load_settings(join(script_path, 'config.ini'))

        super().__init__(conf, script_path)

        self.jinja_env.globals.update(get_user=login.getUser)
        filters.init_jinja_filters(self)

        startup.init(self)
        login.init_login(self, conf['login'])
        mail.init_mail(self, conf['mail'])

        with open('core/content/version.txt') as fh:
            self.version = fh.readline()


if __name__ == "__main__":
    app = ExampleWebsite()
    app.start()
