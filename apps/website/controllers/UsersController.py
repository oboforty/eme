from flask import render_template
from flask import request


class UsersController():
    def __init__(self, server):
        self.server = server
        self.group = "Users"

    def index(self):

        return render_template('/home/index.html')
