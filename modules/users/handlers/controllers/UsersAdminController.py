from email.utils import parseaddr

from flask import render_template, request, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from eme.data_access import get_repo
from modules.easy_mail import mail
from modules.users import auth
from modules.users.dal.UserManager import AuthException
from modules.users.dal.entities.user import User


class UsersController():

    def __init__(self, server):
        self.server = server

    def get_list(self):
        if not current_user.admin:
            return redirect('/users/login')

        users = get_repo(User).list_all()

        return render_template('/users/list.html', users=users)
