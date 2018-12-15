from flask import render_template, request, Response
from flask_login import current_user
from werkzeug.utils import redirect

from website.entities import ApiResponse


class HomeController():
    def __init__(self, server):
        self.server = server
        self.group = "Home"

        # todo: routing setting

        # todo: Api example (chat)

        # self.server.setRouting({
        #     '/home/info': '/info',
        # })

    def index(self):

        if current_user.is_authenticated:
            if current_user.role is None:
                return redirect('client/claim')
        
        else:
            return redirect('users/login')


        return render_template('/home/index.html', err=request.args.get('err'))
