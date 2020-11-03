from flask import Flask
from flaskext.mysql import MySQL

from config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.secret_key = 'soccerSoccersoccer'

mysql = MySQL(app)

from app.public import public_mod
app.register_blueprint(public_mod)

from app.errors import error_mod
