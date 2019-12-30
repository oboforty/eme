from collections import defaultdict

from flask import render_template, request
from werkzeug.utils import redirect

from webapp.services import login

from engine import settings
from game.instance import towns, users
from webapp.entities import ApiResponse
from webapp.services.login import getUser


class UserDevController():
    def __init__(self, server):
        self.server = server
        self.group = "UsersDev"

    def get_list(self):
        user = login.getUser()

        if not user.admin:
            return redirect('/users/login')

        asd = users.list_all(towns=True)
        points = defaultdict(int)
        _users = []

        for user, town in asd:
            _users.append(user)

            if town:
                for bid, lvl in town.buildings.items():
                    points[town.iso] += lvl

                for bid, lvl in town.gatherers:
                    points[town.iso] += lvl

        return render_template('/users/list.html', users=_users, points=points)


    def get_edit(self):
        user = getUser()

        if not user.username or not user.admin:
            return redirect('/users/login')

        # load user to view:
        username = request.args.get('username')
        uid = request.args.get('uid')

        if username is not None:
            my_user = users.find_user(username=username)
        elif uid is not None:
            my_user = users.get(uid)
        else:
            my_user = user

        if not my_user:
            return "not found"

        return render_template('/users/edit.html', uinfo=my_user, conf=settings._conf)

    def post_edit(self):
        user = getUser()

        if not user.username or not user.admin:
            return "no u"

        uid = request.form['uid']
        user = users.get(uid)

        user.admin = request.form["admin"] == '1'
        user.wid = request.form["wid"]
        user.iso = request.form["iso"]
        user.email = request.form["email"]
        user.username = request.form["username"]

        if not user.wid or user.wid == 'None': user.wid = None
        if not user.iso or user.iso == 'None': user.iso = None
        if not user.admin: user.admin = False

        users.save()

        return redirect('/user/list')
