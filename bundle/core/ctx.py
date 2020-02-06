import redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from eme.data_access import register_session
from eme.entities import load_settings

config = load_settings("core/content/ctx.ini")
db_type = config.get('db.type')

# an Engine, which the Session will use for connection resources
if db_type == 'sqlite':
    db_engine = create_engine('sqlite:///{file}'.format(**config[db_type]), connect_args={'check_same_thread': False})
else:
    if 'driver' in config[db_type]:
        db_type += '+' + config[db_type].pop('driver')
    db_engine = create_engine(db_type+'://{user}:{password}@{host}/{database}'.format(**config[db_type]))

Session = sessionmaker(bind=db_engine)

db_session = Session()

register_session('db', db_session)


def set_session(sess):
    global db_session

    db_session.close()
    db_session = sess


def get_session(force=False):
    if force:
        global db_session

        db_session.close()
        db_session = Session()

    return db_session

redis_session = None


def get_redis(force=False):
    global redis_session

    if redis_session is None or force:
        redis_session = redis.StrictRedis(**config['redis'])

    return redis_session

from sqlalchemy.ext.declarative import declarative_base

EntityBase = declarative_base()
