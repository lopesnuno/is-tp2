import os.path
import psycopg2
from psycopg2 import DatabaseError


class Database:
    connection = None
    cursor = None

    def storeFile(self, file_path, db_file_name):
        try:
            with open(os.path.join(file_path), 'r') as file:
                xml = file.read()

            Database.connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            Database.cursor = Database.connection.cursor()
            Database.cursor.execute('''INSERT INTO imported_documents(file_name, xml) VALUES (%s, %s)''', (db_file_name, xml))

            Database.connection.commit()

            return "File stored successfully in the database."

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)
            if Database.connection:
                Database.connection.rollback()
            return f"Error {error}"

        finally:
            if Database.connection:
                Database.cursor.close()
                Database.connection.close()

    def query(self, query):
        try:
            Database.connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')

            print('Connected to database...')
            with Database.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
            print('Cursor executed')
            return result
        except DatabaseError as e:
            return f"DatabaseError: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

        finally:
            if Database.connection:
                Database.connection.close()
                Database.cursor = None

