from core.ctx import dbctx


class MigrateCommand():
    def __init__(self, server):
        self.server = server

    def run(self, *args):
        base = 'commands/migrations/{}.sql'

        conn = dbctx.getConn()
        cur = dbctx.getCursor(conn)

        # expand this for migration
        for f in ['exts', 'users']:
            print('Applying migration {}...'.format(f))
            sql_file = open(base.format(f), 'r')

            cur.execute(sql_file.read())

        conn.commit()
        cur.close()
