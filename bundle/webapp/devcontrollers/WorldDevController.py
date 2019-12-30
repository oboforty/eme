import datetime

from flask import render_template, request
from werkzeug.utils import redirect

from engine import settings

from game.entities import World
from game.instance import towns, users, worlds
from webapp.entities import ApiResponse
from webapp.services.login import getUser


class WorldDevController():
    def __init__(self, server):
        self.server = server
        self.group = "WorldDev"

    def get_list(self):
        user = getUser()

        if not user.username or not user.admin:
            return redirect('/users/login')

        _worlds = worlds.list_all()

        return render_template('/worlds/list.html', worlds=_worlds, conf=settings._conf)


    def get_edit(self):
        user = getUser()

        if not user.username or not user.admin:
            return redirect('/users/login')

        # load user to view:
        wid = request.args.get('wid')

        if wid is None:
            return redirect('/world/list')

        world = worlds.get(wid)

        return render_template('/worlds/edit.html', world=world, conf=settings._conf)


    def post_edit(self):
        user = getUser()

        if not user.username or not user.admin:
            return "no u"

        wid = request.form['wid']

        name = request.form['name']
        invlink = request.form['invlink']
        max_players = request.form['max_players']


        world: World = worlds.get(wid)
        try:
            last_update = datetime.datetime.strptime(request.form['last_update'], '%Y-%m-%d %H:%M:%S')
        except:
            last_update = world.last_update

        world.name = name
        world.invlink = invlink
        world.max_players = max_players
        world.last_update = last_update

        worlds.save()

        return redirect('/')
