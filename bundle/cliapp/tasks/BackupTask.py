import shutil
from datetime import datetime

from eme.entities import loadConfig
from engine import settings


class BackupTask:

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def run(self):
        """
        Backup database
        """

        backup = loadConfig('cliapp/config.ini')['backup']

        dbfile = backup['db_file']
        backupfile = backup['file']

        # backup every day (rename to current week name)
        # backup monthly
        today = datetime.today()

        shutil.copy(dbfile, backupfile.format(year=today.year, month=today.month))
