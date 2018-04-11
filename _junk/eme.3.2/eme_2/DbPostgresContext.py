from enum import Enum

from psycopg2 import connect
from psycopg2 import extras
from psycopg2.pool import SimpleConnectionPool, PersistentConnectionPool, ThreadedConnectionPool


class DbContextType(Enum):
    SingleClient = 1
    SinglePool = 2
    ThreadedPool = 3


class DbPostgresContext():
    def __init__(self, connInfo, client=DbContextType.SingleClient):
        if not isinstance(client, DbContextType):
            self.connType = DbContextType.SingleClient
            self.conn = client
        elif client == DbContextType.SingleClient:
            self.connType = client
            self.conn = connect(**connInfo)
        elif client == DbContextType.SinglePool:
            self.connType = client
            self.conn = SimpleConnectionPool(**connInfo)
        elif client == DbContextType.ThreadedPool:
            self.connType = client
            self.conn = ThreadedConnectionPool(**connInfo)

    def getConn(self):
        if self.connType == DbContextType.SingleClient:
            return self.conn
        else:
            return self.conn.getconn()

    def getCursor(self, conn=None):
        if conn is None:
            conn = self.getConn()
        return conn.cursor(cursor_factory=extras.DictCursor)

    def getDbType(self):
        return 'postgres'
