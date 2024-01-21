import json
import os.path
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify
import xmlrpc.client
import traceback
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def connect_to_server(retry_attempts=5, delay_seconds=2):
    for attempt in range(1, retry_attempts + 1):
        try:
            print(f"Connecting to the server (Attempt {attempt}/{retry_attempts})...")
            server = xmlrpc.client.ServerProxy('http://rpc-server:9000/RPC2')
            print("Connection successful.")
            return server
        except ConnectionError as ce:
            print(f"Error: Unable to connect to the server. {ce}")
        except Exception as e:
            print(f"Error: An unexpected error occurred. {e}")

        if attempt < retry_attempts:
            print(f"Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)

    raise ConnectionError(f"Failed to connect after {retry_attempts} attempts. Please check the connection.")


server = connect_to_server()


@app.route('/api/triple_double_players', methods=['GET'])
@cross_origin()
def api_get_triple_double_players():
    try:
        result = server.get_players_with_tripleDoubleSeasons()
        data = json.loads(result)
        return jsonify(data)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Failed to fetch data from RPC server: {str(e)}"}), 500


@app.route('/api/top5_colleges', methods=['GET'])
@cross_origin()
def api_get_top5_colleges():
    try:
        result = server.get_top5_colleges()
        data = json.loads(result)
        return json.dumps(data, indent=2)
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()  # Add this line to print the traceback
        return jsonify({"error": f"Failed to fetch data from RPC server: {str(e)}"}), 500


if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=8080)