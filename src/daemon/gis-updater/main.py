import sys
import os
import time
import pika
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import psycopg2
from psycopg2 import OperationalError

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
XML_PATH = "/xml"

geolocator = Nominatim(user_agent="is-tp2")


def get_colleges():
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        query = '''SELECT id, name FROM public.colleges WHERE geom IS NULL'''
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except (Exception, psycopg2.Error) as error:
        return f"Error: {error}"
    finally:
        cursor.close()
        connection.close()


# !TODO: 3- Submit the changes
def update_college(college_id, latitude, longitude):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        query = '''UPDATE public.colleges SET latitude = %s, longitude = %s, geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326) WHERE id = %s'''
        cursor.execute(query, (latitude, longitude, latitude, longitude, college_id))
        connection.commit()
    except OperationalError as error:
        return f"Error: {error}"
    finally:
        cursor.close()
        connection.close()


# !TODO: 2- Use the entity information to retrieve coordinates from an external API
def get_coordinates_by_college_name(name, attempt=1, max_attempts=10):
    try:
        location = geolocator.geocode(name)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            print(f"Recursive run: {attempt}/{max_attempts}")
            time.sleep(10)
            return get_coordinates_by_college_name(name, attempt=attempt+1)

        other_colleges = get_colleges()
        return process_colleges_in_pieces(other_colleges)


def process_colleges_in_pieces(colleges, size=ENTITIES_PER_ITERATION):
    num_colleges = len(colleges)

    for i in range(0, num_colleges, size):
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        piece = colleges[i:i + size]
        for college in piece:
            geo = get_coordinates_by_college_name(college[1])
            if geo is not None:
                update_college(college[0], geo[0], geo[1])
                time.sleep(1.3)
        print(f"{ENTITIES_PER_ITERATION} colleges updated...")

    return


if __name__ == "__main__":

    rabbitMqUrl = "amqp://is:is@rabbitmq:5672/is"
    queue_name = "gis_updater"

    connection_params = pika.URLParameters(rabbitMqUrl)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()


    def callback(ch, method, properties, body):
        message = body.decode('utf-8')
        print(f"{message}")
        colleges = get_colleges()
        process_colleges_in_pieces(colleges)
        time.sleep(POLLING_FREQ)


    channel.basic_consume(queue='gis_updater', on_message_callback=callback, auto_ack=True)
    print('Waiting to start GIS updater...')
    channel.start_consuming()



