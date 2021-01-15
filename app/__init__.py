from flask import Flask
from flaskext.mysql import MySQL

from config import Config
import logging.handlers

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/tmp/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.secret_key = 'soccerSoccersoccer'

mysql = MySQL(app)

from app.public import public_mod
app.register_blueprint(public_mod)

from app.errors import error_mod
