from quartz.data.meta import Schema, Table, Column
import quartz.data.base as _base
from quartz.log import Log
from quartz.error import Error
from quartz.data.query import Queries
from abc import ABC, abstractmethod
import mysql.connector
import os


class Database(_base.Database):

    def __init__(self, schema: str, name:str, user:str, password:str):
        super().__init__(schema)
        self._ = None
        self._name = name
        self._user = user
        self._password = password

    def open(self, reset: bool=False):
        self._ = mysql.connector.connect(
            host="localhost",
            user=self._user,
            password=self._password,
            database=self._name)
        if reset:
            self._create()

    def close(self):
        if self._ is not None:
            self._.close()
            self._ = None

    def isOpen(self):
        return self._ is not None

    def meta(self):
        return None

    def sql(self, query, append=None):
        s = super().sql(query, append)
        return s.replace("?", "%s")

    def _exec(self, sql, params=[]):
        # Log.debug(f"SQL:\n{sql}\n{params}")
        cur = self._.cursor()
        cur.execute(sql, params)
        self._.commit()
        return cur.lastrowid

    def _begin(self, sql, params=[]):
        # Log.debug(f"SQL:\n{sql}\n{params}")
        cur = self._.cursor()
        cur.execute(sql, params)
        return cur
    
    def _next(self, cursor):
        return cursor.fetchone()

    def _all(self, sql, params=[]):
        # Log.debug(f"SQL:\n{sql}\n{params}")
        cur = self._.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def _create(self):
        if not os.path.exists(self._schema):
            Error.missing(self._schema)
        with open(self._schema, "r") as f:
            script = f.read()
            cur = self._.cursor()
            for statement in script.split(";"):
                sql = statement.strip()
                if sql:
                    cur.execute(sql)
            self._.commit()