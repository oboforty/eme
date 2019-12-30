from time import sleep

from engine.modules.chat import service as chat_service
from game.instance import worlds



class DisposalTask:

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def run(self):
        # todo: delete AFK worlds (inactivity for more than 6 months)

        return

        # to_delete_worlds = worlds.list_inactive()
        #
        # # dispose worlds
        # for i,world in enumerate(to_delete_worlds):
        #
        #     worlds.delete(world, commit=False)
        #
        #     # clear chat
        #     chat_service.clear(world.wid, 'global')
        #
        #     if i % 20 == 0:
        #         # make sure to save changes every once in a while
        #         worlds.session.commit()
        #
        #         # rest for 80ms
        #         sleep(0.08)
        #
        # worlds.session.commit()
        #
