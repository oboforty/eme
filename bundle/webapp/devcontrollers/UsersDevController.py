from collections import defaultdict
from eme.data_access import get_repo

from flask import render_template, request
from flask_login import current_user
from werkzeug.utils import redirect

from core.dal.users import User
from webapp.entities import ApiResponse
from webapp.services import mail, auth



class UsersDevController():
    def __init__(self, server):
        self.server = server
        self.group = "UsersDev"

    def get_list(self):
        if not current_user.admin:
            return redirect('/users/login')

        users = get_repo(User).list_all()

        return render_template('/users/list.html', users=users)


    def get_edit(self):
        if not current_user.username or not current_user.admin:
            return redirect('/users/login')

        # load user to view:
        username = request.args.get('username')
        uid = request.args.get('uid')
        repo = get_repo(User)

        if username is not None:
            my_user = repo.find_user(username=username)
        elif uid is not None:
            my_user = repo.get(uid)
        else:
            my_user = current_user

        if not my_user:
            return "not found"

        return render_template('/users/edit.html', uinfo=my_user)

    def post_edit(self):
        if not current_user.username or not current_user.admin:
            return redirect('/users/login')
        repo = get_repo(User)

        uid = request.form['uid']
        user = repo.get(uid)

        user.admin = request.form["admin"] == '1'
        user.email = request.form["email"]
        user.username = request.form["username"]
        if not user.admin: user.admin = False

        repo.save()

        return redirect('/user/list')
