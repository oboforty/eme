from flask import render_template, request
from werkzeug.utils import redirect

from engine import settings
from game.instance import towns, users
from webapp.entities import ApiResponse
from webapp.services.login import getUser


class TownDevController():
    def __init__(self, server):
        self.server = server
        self.group = "TownDev"

    def get_edit(self):
        user = getUser()

        if not user.username or not user.admin:
            return redirect('/users/login')

        # load user to view:
        username = request.args.get('username')
        if username is not None:
            my_user = users.find_user(username=username)

            if not my_user:
                return "User not found: {}".format(username)
        else:
            my_user = user

        # load town by loaded user:
        wid = request.args.get('wid', my_user.wid)
        iso = request.args.get('iso', my_user.iso)
        town = towns.get(iso, wid=wid)

        return render_template('/towns/edit.html', town=town,wid=wid,iso=iso, conf=settings._conf)

    def post_edit(self):
        user = getUser()

        if not user.username or not user.admin:
            return "no u"

        wid = request.form['wid']
        iso = request.form['iso']
        resources = request.form['resources']
        gatherers = request.form['gatherers']
        placements = request.form['placements']
        buildings = request.form['buildings']

        town = towns.get(iso, wid=wid)

        town.resources = resources
        town.gatherers = gatherers
        town.placements = placements
        town.buildings = buildings

        towns.save()

        return ApiResponse({
            "ok": True
        })
