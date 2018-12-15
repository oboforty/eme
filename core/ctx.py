import configparser

import redis
from crudible.db.postgres import PostgresContext, ClientType
from core.eme import loadConfig


config = loadConfig("core/content/ctx.ini")

# Redis
#redisctx = redis.Redis(**config['redis'])

# Postgres
if config['db'].pop('type') != 'postgres':
    raise Exception("DB type was not meant to be postgres ({}).".format(config['db']['type']))

dbctx = PostgresContext(config['db'], client=ClientType.SingleClient)


def getContext():
   return dbctx
