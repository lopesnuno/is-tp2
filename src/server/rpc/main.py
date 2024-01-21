import signal
import sys
import logging
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
from functions.string_length import string_length
from functions.string_reverse import string_reverse
from functions.manage_files import import_csv
from functions.queries import get_highest_scoring_season_by_player, get_players_with_tripleDoubleSeasons, \
    get_top5_colleges

# Configure logging
logging.basicConfig(level=logging.INFO)

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def log_request(self, code='-', size='-'):
        logging.info(f"Request received: {self.requestline}")

with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()
    server.allow_none = True

    def signal_handler(signum, frame):
        logging.info("Received signal")
        server.server_close()

        # Perform clean up, etc. here...

        logging.info("Exiting, gracefully")
        sys.exit(0)

    # Signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Register functions
    server.register_function(string_reverse)
    server.register_function(string_length)
    server.register_function(import_csv)
    server.register_function(get_highest_scoring_season_by_player)
    server.register_function(get_players_with_tripleDoubleSeasons)
    server.register_function(get_top5_colleges)

    # Start the server
    logging.info("Starting the RPC Server...")
    server.serve_forever()
