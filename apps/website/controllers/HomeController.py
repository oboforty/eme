from flask import render_template
from flask import request


class HomeController():
    def __init__(self, server):
        self.server = server
        self.group = "Home"

    def index(self):
        return render_template('/home/index.html')
