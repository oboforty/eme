from flask import render_template, request, Response

from core.dal.users import User
from eme.data_access import get_repo


class ExamplesController:
    """
    This controller is only used to illustrate various capabilities of EME.
    The different ways you can map routes are:

    1. using a decorator, just like in Flask
    2. in the __init__ of a Controller (app.preset_endpoints)
    3. in the config.ini
    """
    def __init__(self, app):
        self.app = app

        # by default, the Examples.custom_route2 endpoint would be reached at 'localhost:5000/examples/custom_route2'
        # with the rule below, however, the new url is 'localhost:5000/example2'
        self.app.preset_endpoints({
            'GET /example2': 'Examples.custom_route2',
        })

        self.users = get_repo(User)

        # you can of course put this in a separated code, without the class
        @app.route('/example1')
        def custom_route1():
            return render_template('/examples/custom_route.html', route=1)

    def custom_route2(self):
        return render_template('/examples/custom_route.html', route=2)

    def custom_route3(self):
        return render_template('/examples/custom_route.html', route=3)
