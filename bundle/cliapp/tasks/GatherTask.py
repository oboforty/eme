from game.services import gatherers
from game.instance import worlds
from game.instance import towns
import datetime


class GatherTask:

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def run(self):
        _worlds = worlds.list_all()

        for world in _worlds:
            time_now = datetime.datetime.utcnow()
            dt = (time_now - world.last_update).seconds

            MSG = '\n{} at {}. dT = {} hrs\n'.format(world.wid, time_now.ctime(), dt/3600.0)

            for town in world.towns:
                dres = town.resources.copy()

                try:
                    gatherers.update_resources(town, dt)
                    towns.mark_changed(town)

                    dres = {k: round(town.resources[k]-v, 6) for k,v in dres.items()}
                except Exception:
                    self.scheduler.logger.exception("ERR in {}/{} -- GATH: {}".format(town.iso, world.wid, dres))

                MSG += ('  {}:   {}\n'.format(town.iso, dres))

            if self.scheduler.logger:
                self.scheduler.logger.debug(MSG)

            world.last_update = time_now

        # save session for all entities
        worlds.save()
