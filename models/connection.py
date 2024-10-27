
import pymysql
from utils.macros import DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_USER

class connection_db:

    def __init__(self):
        self.DATABASE = "EdSquared_db"
        self.conn = None

    def establish_conn(self):
        # Using pymysql.connect to get a connection object 
        timeout = 10
        try:
            self.conn = pymysql.connect(
              charset="utf8mb4",
              connect_timeout=timeout,
              cursorclass=pymysql.cursors.DictCursor,
              db="defaultdb",
              host=DATABASE_HOST,
              password=DATABASE_PASSWORD,
              read_timeout=timeout,
              port=DATABASE_PORT,
              user=DATABASE_USER,
              write_timeout=timeout,
            )
            self.conn.autocommit(True)
            print(f"Connection Established to Database: {self.DATABASE}")
        except pymysql.MySQLError as e:
            print(f"Error Establishing connection to Database: {self.DATABASE} Error: {e}")

    def check_and_reconnect(self):
        #Checks the current database connection by pinging the server. If the connection is lost, attempts to
        #re-establish it by calling the establish_conn() method
        try:
            self.conn.ping(reconnect=True)
        except pymysql.MySQLError as e:
            print(f"Error pinging database: {e}")
            self.establish_conn()
        except Exception as e:
            print(e)
            self.establish_conn()

    def close_conn(self):
        # Closes the current connection to the MySQL database
        if self.conn:
            self.conn.close()
            print(f"Connection for database: {self.DATABASE} closed.")
###
    def execute_query(self, query, params=None):
        # Executes the queries which make changes to the database (alter, modify, insert, update, delete...)
        if not self.conn:
            self.establish_conn()

        if self.conn:
            self.check_and_reconnect()

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            self.conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Error executing query: {query} Error: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

    def fetch_response(self, query, params=None, response_type=None):
        # Executes the queries which fetches data/rows from the database (select)
        if not self.conn:
            self.establish_conn()

        if self.conn:
            self.check_and_reconnect()

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            if response_type == 1:
                result = cursor.fetchone()
                return result
            elif response_type == 0:
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"Error executing query: {query} Error: {e}")
            raise
        finally:
            cursor.close()
