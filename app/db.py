import pymysql

from app import mysql
from config import Config


def query(db=Config.MYSQL_DATABASE_DB, statement="required", vars="", dictResults=False):
    """
    Executes the statement and then returns the result as a list
    Statement - SQL Query
    Vars - List of variables in Query to prevent SQL Injection
    """

    # not using variable dictResults for now.  Always getting dictResults
    cur = get_connection().cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    if Config.SHOW_QUERIES:
        log_print("QUERY", db, statement, vars)

    result = cur.fetchall()
    cur.connection.commit()
    return result


# only searches for one return option/value
def query_one(db=Config.MYSQL_DATABASE_DB, statement="required", vars="", dictResults=False):
    """
    Executes the statement and then returns the the first row of the result
    Statement - SQL Query
    Vars - List of variables in Query to prevent SQL Injection
    """

    # not using variable dictResults for now.  Always getting dictResults
    cur = get_connection().cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    if Config.SHOW_QUERIES:
        log_print("QUERY", db, statement, vars)
    return cur.fetchone()


def insert(db=Config.MYSQL_DATABASE_DB, statement="required", vars=None):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    cur.execute(statement, vars)

    cur.connection.commit()

    if Config.SHOW_QUERIES:
        log_print("INSERT", db, statement, vars)

def insertmany(db=Config.MYSQL_DATABASE_DB, statement="required", data=None):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    cur.executemany(statement, data)

    cur.connection.commit()

    if Config.SHOW_QUERIES:
        log_print("INSERT", db, statement, data)


def update(db=Config.MYSQL_DATABASE_DB, statement="required", vars="", display=False):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    cur.connection.commit()

    if display:
        log_print("UPDATED", db, statement, vars)


def delete(db=Config.MYSQL_DATABASE_DB, statement="required", vars="", display=False):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    cur.connection.commit()

    if display:
        log_print("DELETE", db, statement, vars)

def get_connection():
    return pymysql.connect(
        host=Config.MYSQL_DATABASE_HOST,
        user=Config.MYSQL_DATABASE_USER,
        passwd=Config.MYSQL_DATABASE_PASSWORD,
        db=Config.MYSQL_DATABASE_DB,
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor)

def use_db(cur, db, display=False):
    if display:
        print("Using db, %s" % db)
    cur.execute('USE ' + str(db))

def log_print(operation, db, statement, values):
    print("%s @ %s: '%s', %s " % (operation, db, statement, values))