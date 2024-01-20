import sys
import time
import psycopg2
from psycopg2 import OperationalError
import xml.etree.ElementTree as ET

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 120


def check_updates(cursor, last_check):
    query = f"SELECT * FROM imported_documents WHERE updated_on > %s OR created_on > %s;"
    cursor.execute(query, (last_check, last_check))
    data = cursor.fetchall()
    if data:
        return data
    else:
        return None

def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_org is None or db_dst is None:
            sys.exit("Failed to connect to the database.")

        # !TODO: 1- Execute a SELECT query to check for any changes on the table

        last_check = '2024-01-19 00:00:00'

        try:
            with db_org.cursor() as cursor:
                while last_check:
                    results = check_updates(cursor, last_check)
                    if results is not None:
                        unique_colleges = set()
                        for row in results:
                            xml_data = row[2]
                            try:
                                root = ET.fromstring(xml_data)
                                colleges = [college.find("College/name").text for college in root.findall(".//Player")]
                                # !TODO: 2 - Retreive info that will be added in db-rel
                                for name in colleges:
                                    if name is not None:
                                        if name not in unique_colleges:
                                            unique_colleges.add(name)


                            except ET.ParseError as e:
                                print("Error parsing XML data:", e)

                        time.sleep(1)

                    else:
                        print('No results.')

                    last_check = time.strftime('%Y-%m-%d %H:%M:%S')
                    time.sleep(POLLING_FREQ)

        except OperationalError as err:
            print_psycopg2_exception(err)
        finally:
            db_org.close()


        # !TODO: 3- Execute INSERT queries in the destination db
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        db_org.close()
        # db_dst.close()