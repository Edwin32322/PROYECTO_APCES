from decouple import config
from flask_mysqldb import MySQLdb

#Conexión a base de datos con Flask-MySqldb
def get_connection():
    try:
        connection = MySQLdb.connect(
            host = config('MYSQL_HOST'),
            user = config('MYSQL_USER'),
            password = config('MYSQL_PASSWORD'),
            db = config('MYSQL_DB')
        )
        return connection
    except MySQLdb.Error as ex:
        raise ex