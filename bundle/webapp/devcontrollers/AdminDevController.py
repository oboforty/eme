import os

from flask import render_template, request

from engine import settings
from werkzeug.utils import redirect

from game.instance import towns
from webapp.services.login import getUser


class AdminDevController():
    def __init__(self, server):
        self.server = server
        self.group = "AdminDev"

    def index(self):
        user = getUser()

        if not user.username or not user.admin:
            return redirect('/users/login')

        if user.uid == 'None':
            raise Exception("hifga yayaya")

        return render_template('/admin/index.html',
            conf=settings._conf,
            err=request.args.get('err')
        )

    def get_viewer(self):
        user = getUser()

        if not user.username or not user.admin:
            return redirect('/users/login')

        model = request.args.get('model', "test/boombox.glb")
        models = []

        exts3d = ['.glb', '.babylon', '.obj', '.fbx', '.stl']

        rootdir = 'webapp/public/models'
        for root, subdirs, files in os.walk(rootdir):
            for f in files:
                fpath = os.path.join(root, f)
                _, ext = os.path.splitext(f)

                if ext in exts3d:
                    models.append((f, fpath[len(rootdir):]))

        return render_template('/admin/viewer.html', model=model, models=models)

    def get_infobar(self):
        user = getUser()

        if not user.username or not user.admin:
            return redirect('/users/login')

        town = towns.get(user.iso, wid=user.wid)

        return render_template('/admin/infobartest.html', town=town, conf=settings._conf)
