import logging
import re
from email.utils import parseaddr

from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, request
from flask_login import LoginManager, login_required, login_user, logout_user

#from core.auth import UserManager, UserException
#from website.entities import UserAuth

#loginManager = LoginManager()
#userManager = UserManager()

#def get_403(e):
#    return Response('<p>Login failed</p>')

#@loginManager.user_loader
#def load_user(userid):
#    return UserAuth(userManager.getUser(userid))


class UsersController():
    def __init__(self, server):
        self.server = server
        self.group = "Users"

        # Init login
        self.server.config["SECRET_KEY"] = "MY_VERY_SECRET_KEY"
        #self.loginManager = loginManager
        #self.loginManager.init_app(server)
        #self.loginManager.login_view = "get_users/login"

        # Init user storage
        #self.manager = userManager


    @login_required
    def profile(self):
        return render_template('/users/index.html')

    def post_login(self):
        email = request.form['email']
        password = request.form['password']
        remember = bool(request.form.get('remember'))

        paddr = parseaddr(email)
        if not paddr[1] == email:
            raise Exception("Email is not valid")

        try:
            user = self.manager.authenticateCredentials(email, password)
            if user:
                authUser = UserAuth(user)
                login_user(authUser, remember=remember)
                next = request.args.get("next")
                if next:
                    return redirect(next)
                else:
                    return redirect('/')
        except UserException as e:
            return redirect('/users/login&err={}'.format(e.code))
        except Exception as e:
            logging.exception("AUTH:LOGIN")
            raise e

    def get_login(self):
        return render_template('/users/login.html', err=request.args.get('err'))

    def post_register(self):
        try:
            user = self.manager.create(request.form.to_dict())

            return redirect('/users/login')
        except UserException as e:
            return redirect('/users/register&err={}'.format(e.code))
        except Exception as e:
            logging.exception("AUTH:REGISTER")
            raise e

    def get_register(self):
        return render_template('/users/register.html', err=request.args.get('err'))

    @login_required
    def get_logout(self):
        logout_user()
        return redirect('/users/login')
