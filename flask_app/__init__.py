from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes