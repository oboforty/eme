import logging

from engine import settings
from eme.entities import loadHandlers, loadConfig


class Scheduler():

    def __init__(self):
        self.tasks = loadHandlers(self, 'Task', prefix='cliapp/')

        self.conf = loadConfig('cliapp/config.ini')['scheduler']

        # Logging
        logger = logging.getLogger('geosch')
        logger.setLevel(logging.DEBUG)

        # file log
        fh = logging.FileHandler(self.conf['logfile'])
        lvl = self.conf.get('loglevel', 'WARNING')
        fh.setLevel(getattr(logging, lvl))

        # console log
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

        self.logger = logger

        self.debug_log = settings.get('server.scheduler_log_deep', None, False)

    def run(self, tasks=None):
        if tasks is None:
            # all tasks
            tasks = self.tasks.keys()

        for name in tasks:
            self.tasks[name].run()
