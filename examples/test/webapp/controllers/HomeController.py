from flask import render_template


class HomeController():
    def __init__(self, server):
        self.server = server

    def welcome(self):
        return render_template('/home/index.html')
