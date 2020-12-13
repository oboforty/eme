from modules.eme_utils.services.migrations import migrate_db


class MigrateCommand:
    """
    Command to run migrations on database.
    """
    def __init__(self, cli):
        self.conf = cli.conf['migration']

    def run(self):
        migrate_db()
