
#import psycopg2
#import psycopg2.extras
import json

from vendor.eme.EntityPatch import EntityPatch


class Repository():
    table = ""
    select = "*"
    insertFields = ""
    prefix = ""
    join = None
    primary = "id"
    ctx = None
    delim = '' # postgres = ""

    def find(self, id):
        condi = {}

        if not isinstance(self.primary, list):
            condi[self.primary] = id
        else:
            for i in range(0, len(self.primary)):
                condi[self.primary[i]] = id[i]
        return self.findBy(**condi)

    def findBy(self, multiple=False, **kwargs):
        conditions = []
        placeholders = []

        for field, value in kwargs.items():
            fname = self.prefix + "."+field if self.prefix else field
            conditions.append(fname + ' = %s')
            placeholders.append(value)
        table = self.table + " " + self.prefix if self.prefix else self.table

        cur = self.ctx.getCursor()
        sql = "select {} from {} {} where {}".format(self.select, table, "left join " + self.join if self.join else "", ' and '.join(conditions))

        cur.execute(sql, tuple(placeholders))

        if not multiple:
            result = cur.fetchone()

            if result is None:
                return None
            return EntityPatch(result)
        else:
            results = cur.fetchall()
            return [EntityPatch(result) for result in results]

    def edit(self, ids, entity=None, **kwargs):
        updates = []
        uplaceholders = []
        conditions = []

        if entity is not None:
            if isinstance(entity, dict):
                kwargs = entity
            elif isinstance(entity, EntityPatch):
                kwargs = entity.entityDict

        if isinstance(self.primary, list):
            ids = list(ids)
            for field in self.primary:
                conditions.append(field + ' = %s')
        else:
            conditions = [self.primary + ' = %s']
            ids = [ids]

        for field, value in kwargs.items():
            if isinstance(value, dict) or isinstance(value, list):
                value = json.dumps(value)

            updates.append(self.delim+ field + self.delim+' = %s')
            uplaceholders.append(value)

        conn = self.ctx.getConn()
        cur = self.ctx.getCursor(conn)
        sql = "update {} set {} where {}".format(self.table, ','.join(updates), ' and '.join(conditions))
        cur.execute(sql, tuple(uplaceholders + ids))
        conn.commit()
        cur.close()

    def all(self):
        pass

    def create(self, **kwargs):
        placeholders = []
        fields = []

        for field in self.insertFields:
            if field in kwargs and kwargs[field] is not None:
                value = kwargs[field]

                if isinstance(value, dict) or isinstance(value, list):
                    value = json.dumps(value)
                #if isinstance(value, str):
                #    value = value.encode('utf-8')
                fields.append(self.delim+field+self.delim)
                placeholders.append(value)

        conn = self.ctx.getConn()
        cur = self.ctx.getCursor(conn)

        dbtype = self.ctx.getDbType()
        if dbtype == 'postgres':
            sql = "insert into {} ({}) VALUES ({}) RETURNING {}".format(self.table, ','.join(fields), ','.join(['%s'] * len(fields)), self.primary)
            cur.execute(sql, tuple(placeholders))
            eid = cur.fetchone()[0]
        elif dbtype == 'mysql':
            sql = "insert into {} ({}) VALUES ({})".format(self.table, ','.join(fields), ','.join(['%s']*len(fields)))
            cur.execute(sql, tuple(placeholders))
            eid = cur.lastrowid

        conn.commit()
        cur.close()
        return eid

    def delete(self, ids):
        conditions = []

        if isinstance(self.primary, list):
            ids = list(ids)
            for field in self.primary:
                conditions.append(field + ' = %s')
        else:
            conditions = [self.primary + ' = %s']
            ids = [ids]

        conn = self.ctx.getConn()
        cur = self.ctx.getCursor(conn)
        sql = "delete from {} where {}".format(self.table, ' and '.join(conditions))

        cur.execute(sql, tuple(ids))

        conn.commit()
        cur.close()
        return True

    def isPrimary(self, field):
        if isinstance(self.primary, str):
            return self.primary == field
        else:
            return field in self.primary
