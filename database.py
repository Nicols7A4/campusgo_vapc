# import pymysql
# pymysql.install_as_MySQLdb()

import MySQLdb as dbc
import MySQLdb.cursors
from config import Config

def get_connection():
    # Parámetros base
    conn_params = {
        "host": Config.MYSQL_HOST,
        "port": Config.MYSQL_PORT,
        "user": Config.MYSQL_USER,
        "passwd": Config.MYSQL_PASSWORD,
        "db": Config.MYSQL_DATABASE,
        "charset": "utf8mb4",
        "cursorclass": MySQLdb.cursors.DictCursor,
        "autocommit": False
    }
    # Si no es localhost, habilitamos SSL (requerido por TiDB Cloud)
    if Config.MYSQL_HOST not in ["localhost", "127.0.0.1"]:
        conn_params["ssl_mode"] = "VERIFY_IDENTITY"
    return dbc.connect(**conn_params)