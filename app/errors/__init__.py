from app import application
from flask import redirect, Blueprint

error_mod = Blueprint('errors', __name__, url_prefix='')

@application.errorhandler(404)
def unknown(e):
    return redirect('/')