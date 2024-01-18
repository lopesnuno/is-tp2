import os.path
import psycopg2
from psycopg2 import DatabaseError


def storeFile_imported_documents(file_path):
    global connection, cursor
    try:
        with open(os.path.join(file_path), 'r') as file:
            xml = file.read()
        connection = psycopg2.connect(host='db-xml',
                                      database='is',
                                      user='is',
                                      password='is')

        cursor = connection.cursor()
        cursor.execute('''INSERT INTO imported_documents(file_name, xml) VALUES (%s, %s)''', (file_path, xml))

        connection.commit()

        return "File stored successfully in the database."

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)
        connection.rollback()
        return "Error {error}".format(error=error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def storeFile_converted_documents(csv, xml):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-xml',
                                      database='is',
                                      user='is',
                                      password='is')

        cursor = connection.cursor()
        cursor.execute('''INSERT INTO converted_documents(src, file_size, dst) VALUES (%s, %s, %s)''', (csv, os.path.getsize(csv), xml))

        connection.commit()

        return "File stored successfully in the database."

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)
        connection.rollback()
        return "Error {error}".format(error=error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_db_converted_files():
    global connection, cursor, converted_documents
    converted_documents = []
    try:
        connection = psycopg2.connect(host='db-xml',
                                      database='is',
                                      user='is',
                                      password='is')

        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM converted_documents''')
        data = cursor.fetchall()
        for doc in data:
            converted_documents.append(doc[0])

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)
        connection.rollback()
        return "Error {error}".format(error=error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return converted_documents


def query(self, query):
    global connection, cursor

    try:
        connection = psycopg2.connect(host='db-xml',
                                      database='postgres',
                                      user='is',
                                      password='is')

        print('Connected to database...')
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        print('Cursor executed')
        return result
    except DatabaseError as e:
        return f"DatabaseError: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    finally:
        cursor.close()
        connection.close()