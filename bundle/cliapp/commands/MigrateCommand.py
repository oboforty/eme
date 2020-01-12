import os

from sqlalchemy import text

from cliapp.migrations.extra import create_testentities
from cliapp.migrations.guard import check_db, clear_db

from core.ctx import db_session, db_type, db_engine, EntityBase


class MigrateCommand:
    def __init__(self, cli):
        self.commands = {
            'migrate': {
                'help': 'Run migrations for server',
                'short': {},
                'long': []
            }
        }

    def run(self):
        # check if DB is populated
        if not check_db():
            print("The database is not empty. Delete it? Y/n:", end="")
            if input().lower() == 'y':
                print("Clearing DB")
                clear_db()

        base = 'cliapp/migrations/'+db_type+'/'
        try:
            files = os.listdir(base)
        except:
            files = []

        conn = db_session.connection()

        # SQLAlchemy migration
        print("Applying SQLAlchemy migrations...")
        EntityBase.metadata.create_all(db_engine)

        # SQL-based migrations
        for f in files:
            print('Applying migration {}...'.format(f))
            self.runMigration(conn, f)

        print("Add test entities? Y/n:", end="")
        if input().lower() == 'y':
            create_testentities()

        print("Done")

    def runMigration(self, conn, f):
        base = 'cliapp/migrations/'+db_type+'/'

        with open(os.path.join(base, f), 'r') as sql_file:
            sql = text(sql_file.read())

        result = conn.execute(sql)

        db_session.commit()
        conn.close()

