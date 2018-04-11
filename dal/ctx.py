import json

from crudible.db.postgres import PostgresContext

dbconfig = json.load(open('dal/config/db.json'))
dbctx = PostgresContext(dbconfig)

def getContext():
    return dbctx
