from app import app
from flask import redirect, Blueprint

error_mod = Blueprint('errors', __name__, url_prefix='')

@app.errorhandler(404)
def unknown(e):
    return redirect('/')