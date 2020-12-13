import shutil
from datetime import datetime


class BackupCommand:

    def __init__(self, cli):
        self.conf = cli.conf['backup']

    def run(self):
        """
        Backup database
        """

        dbfile = self.conf['db_file']
        backupfile = self.conf['file']

        # backup every day (rename to current week name)
        # backup monthly
        today = datetime.today()

        shutil.copy(dbfile, backupfile.format(year=today.year, month=today.month))
