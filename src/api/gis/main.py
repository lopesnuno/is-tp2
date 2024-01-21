import json
import sys
import psycopg2
from flask import Flask, request
from flask_cors import CORS, cross_origin

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True

connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
cursor = connection.cursor()


@app.route('/api/markers', methods=['GET'])
@cross_origin()
def get_markers():
    args = request.args

    query = '''
    SELECT
    json_build_object(
       'type',  'Feature',
       'geometry', ST_AsGeoJson(c.geom)::jsonb,
       'properties', to_jsonb( c.* ) - 'geom' - 'latitude' - 'longitude'
    ) as json
    FROM
        colleges as c
    WHERE
        c.geom IS NOT NULL
    '''

    cursor.execute(query)
    data = [row[0] for row in cursor.fetchall()]

    return data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
