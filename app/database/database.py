import os
from playhouse.pool import PooledMySQLDatabase
from configuration import *
from peewee import *

if os.path.exists('filestorage.db'):
    os.remove('filestorage.db')

base = PooledMySQLDatabase(
    "filestorage", user=MYSQL_USER, host=MYSQL_HOST, port=MYSQL_PORT, password=MYSQL_PASSWORD,
    max_connections=10, stale_timeout=3600)


class BaseModel(Model):  # klasa bazowa
    class Meta:
        database = base
