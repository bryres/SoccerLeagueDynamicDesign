import os

class Config(object):
    DEBUG=bool(os.environ['SOCCER_DEBUG'])
    SHOW_QUERIES=bool(os.environ['SOCCER_SHOW_QUERIES'])
    SECRET_KEY=os.environ['SOCCER_SECRET_KEY']

    MYSQL_DATABASE_HOST=os.environ['SOCCER_DB_HOST']
    MYSQL_DATABASE_DB=os.environ['SOCCER_DB_SCHEMA']
    MYSQL_DATABASE_USER=os.environ['SOCCER_DB_USER']
    MYSQL_DATABASE_PASSWORD=os.environ['SOCCER_DB_PASSWORD']
    MYSQL_DATABASE_PORT=int(os.environ['SOCCER_DB_PORT'])
