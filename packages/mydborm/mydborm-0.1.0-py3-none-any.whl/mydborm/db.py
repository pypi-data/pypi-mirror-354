import mysql.connector
import psycopg2

class Database:
    connection = None
    cursor = None

    @classmethod
    def connect(cls, engine, **kwargs):
        if engine == "mysql":
            cls.connection = mysql.connector.connect(**kwargs)
        elif engine == "yugabyte":
            cls.connection = psycopg2.connect(**kwargs)
        cls.cursor = cls.connection.cursor()

    @classmethod
    def execute(cls, query, params=None):
        cls.cursor.execute(query, params or [])
        cls.connection.commit()
        return cls.cursor
