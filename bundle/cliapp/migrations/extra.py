from engine.modules.auth.UserManager import UserException, UserManager
from game.instance import users, worlds, towns, areas
from game.services.worldhandling import create_world

userManager = UserManager(users)

def create_testentities():
    # Create test world
    world, _towns, _areas = create_world(name='Hellas')
    world2, _towns2, _areas2 = create_world(name='Hellas 2')

    # insert into DB
    worlds.create(world)
    towns.create_all(_towns)
    if _areas: areas.create_all(_areas)

    worlds.create(world2)
    towns.create_all(_towns2)
    if _areas: areas.create_all(_areas2)


    usrs = [
        ('geo', 'geo@geo.com', 'geo', 'RH', False),
        ('rajmund', 'rajmund.csombordi@hotmail.com', 'hotmail', 'TH', True),
        ('Esteban', 'esteban@gmail.com', 'holyshit', 'OL', True),
        ('Redcard', 'redcard@hotmail.com', 'hotmail', 'SP', True),
    ]

    for username, email, pw, iso, adm in usrs:
        user = userManager.create(username=username, email=email, admin=adm, **{
            'password': pw,
            'password-confirm': pw
        })

        if username == 'geo':
            users.set_world(user.uid, world2.wid, iso)
        else:
            users.set_world(user.uid, world.wid, iso)
