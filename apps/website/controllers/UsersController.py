from flask import render_template
from flask import request

from flask import Flask, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

users = [User(id) for id in range(1, 21)]

manager = LoginManager()

class UsersController():
    def __init__(self, server):
        self.server = server
        self.group = "Users"

        self.server.config["SECRET_KEY"] = "MY_VERY_SECRET_KEY"
        self.manager = manager
        self.manager.init_app(self.server)
        self.manager.login_view = "get_users/login"

    @login_required
    def profile(self):
        return render_template('/users/index.html')

    def post_login(self):
        email = request.form['email']
        password = request.form['password']
        remember = bool(request.form['remember'])

        if password == 'hotmail' and email == 'test@gmail.com':
            user = User(2)
            login_user(user, remember=remember)
            return redirect(request.args.get("next"))
        else:
            return abort(401)

    def get_login(self):
        return render_template('/users/login.html')

    @login_required
    def get_logout(self):
        logout_user()
        return Response('<p>Logged out</p>')

    def get_403(e):
        return Response('<p>Login failed</p>')

    @manager.user_loader
    def load_user(userid):
        return User(userid)
