from flask import render_template, request, Response

from core.dal.users import User
from eme.data_access import get_repo


class HomeController():
    def __init__(self, server):
        self.server = server
        self.group = "Home"

        # routing: url -> endpoint mapping
        self.server.preset_endpoints({
            # by default, the Home.hello endpoint would be reached at 'localhost:5000/home/hello'
            # with this rule, however, the new rule is 'localhost:5000/hello'
            'GET /hello': 'Home.hello',
        })

        self.users = get_repo(User)

    def index(self):

        return render_template('/home/index.html')

    def hello(self):
        return render_template('/home/hello.html')

    def post_hello(self):
        return ''
