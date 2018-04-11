import MySQLdb
import logging
from MySQLdb import cursors


class DbMysqlContext():
    def __init__(self, connInfo):
        self.connInfo = connInfo
        self.connInfo['cursorclass'] = cursors.DictCursor
        self.reconnect()

    def getConn(self):
        #if not self.conn:
        #    logging.error("MYSQL_NOT_CONNECTED")
        #    self.reconnect()
        self.reconnect()
        return self.conn

    def getCursor(self, conn=None):
        if conn is None:
            conn = self.getConn()
        return conn.cursor()

    def reconnect(self):
        self.conn = MySQLdb.connect(**self.connInfo)

    def getDbType(self):
        return 'mysql'
