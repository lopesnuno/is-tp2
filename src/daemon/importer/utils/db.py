import psycopg2
from decouple import config


class PostgresDB:
    def __init__(self, host, port, database, user, password):
        self.curr = None
        self.conn = None
        self.create_connection(host, port, database, user, password)

    def create_connection(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.curr = self.conn.cursor()

    def close_connection(self):
        if self.conn:
            self.curr.close()
            self.conn.close()

    def execute_query(self, query, parameters=None):
        try:
            if parameters:
                self.curr.execute(query, parameters)
            else:
                self.curr.execute(query)

            result = self.curr.fetchall()
            if not result:
                return []

            return result

        except psycopg2.DatabaseError as exception:
            self.conn.rollback()
            self.close_connection()
            raise Exception(exception)


class PostgresTransaction:
    def __init__(self, host, port, database, user, password):
        self.connection = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = None

    def __enter__(self):
        self.connection.autocommit = False
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.connection.commit()
            print("Transaction committed successfully!")
        else:
            self.connection.rollback()
            print(f"Transaction rolled back. Error: {exc_type}: {exc_value}")

        self.cursor.close()
        self.connection.close()
