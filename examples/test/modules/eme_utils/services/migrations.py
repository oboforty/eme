import os
from sqlalchemy import text

from eme.data_access import get_repo

from core.ctx import db_session, db_type, db_engine
from core.base import EntityBase

from modules.eme_utils.services.fixtures import create_testentities
from modules.users.dal.entities.user import User


def check_db():
    try:
        w = get_repo(User).is_empty()
        return not w
    except:
        pass

    return True

def clear_db():
    get_repo(User).delete_all()

    # implement your own calls to clear the database

def migrate_db():
    # check if DB is populated
    if not check_db():
        print("The database is not empty. Delete it? Y/n:", end="")
        if input().lower() == 'y':
            print("Clearing DB")
            clear_db()

    base = 'modules/eme_utils/migrations/' + db_type + '/'
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
        run_sql_migration(conn, f)

    print("Add test entities? Y/n:", end="")
    if input().lower() == 'y':
        create_testentities()

    print("Done")


def run_sql_migration(conn, f):
    base = 'modules/eme_utils/migrations/' + db_type + '/'

    with open(os.path.join(base, f), 'r') as sql_file:
        sql = text(sql_file.read())

    result = conn.execute(sql)

    db_session.commit()
    conn.close()

