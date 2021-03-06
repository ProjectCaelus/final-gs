import json
from handler import Handler

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit, Namespace
import time
import logging

import argparse

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

config = {}

parser = argparse.ArgumentParser(description='Run the Project Caelus Ground Station Server.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--config', help="The config file to use for the simulation (enter " + 
        "local if you want to run the simulation on the default local config). \n" + 
        "Default: config.json")

args = parser.parse_args()

if args.config == "local":
    config = json.loads(open("config.json").read())
    config["telemetry"]["GS_IP"] = "127.0.0.1"
    config["telemetry"]["SOCKETIO_HOST"] = "127.0.0.1"
elif args.config != None:
    try:
        config = json.loads(open(args.config).read())
    except:
        raise Exception("Error reading from config file '" + args.config + "'")
else:
    config = json.loads(open("config.json").read())


app = Flask(__name__, static_folder="templates")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

time.sleep(1)

if __name__ == "__main__":
    
    handler = Handler('/')
    handler.init(config)
    handler.begin()
    print("listening and sending")

    socketio.on_namespace(handler)
    socketio.run(app, host=config["telemetry"]["SOCKETIO_HOST"], port=int(config["telemetry"]["SOCKETIO_PORT"]))
