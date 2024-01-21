from flask import Flask, jsonify
import xmlrpc.client
import traceback

app = Flask(__name__)

# XML-RPC server details
XMLRPC_SERVER_HOST = "rpc-server"  # Use the container name or IP address
XMLRPC_SERVER_PORT = 9000

# XML-RPC proxy
xmlrpc_proxy = xmlrpc.client.ServerProxy(f"http://{XMLRPC_SERVER_HOST}:{XMLRPC_SERVER_PORT}/RPC2")

@app.route('/api/triple_double_players', methods=['GET'])
def api_get_triple_double_players():
    try:
        # Use the RPC server to get data
        result = xmlrpc_proxy.get_players_with_tripleDoubleSeasons()
        return jsonify(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Failed to fetch data from RPC server: {str(e)}"}), 500
    
@app.route('/api/top5_colleges', methods=['GET'])
def api_get_top5_colleges():
    try:
        # Use the RPC server to get data
        result = xmlrpc_proxy.get_top5_colleges()
        return jsonify(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()  # Add this line to print the traceback
        return jsonify({"error": f"Failed to fetch data from RPC server: {str(e)}"}), 500


if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=8080)
