from flask import render_template, request, Response



class HomeController():
    def __init__(self, server):
        self.server = server
        self.group = "Home"

        # old way: weird and inconsistent
        self.server.setRouting({
            #'GET /home/hello': '/hello',
        })

        # new way: url -> endppoint, consistent and allows redundant urls!
        self.server.addUrlRule({
            'GET /hello': 'home/hello',
            'GET /hi': 'home/hello',
        })

    def index(self):

        return render_template('/home/index.html')

    def hello(self):

        return render_template('/home/hello.html')
