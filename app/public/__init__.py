from flask import Blueprint

public_mod = Blueprint('public', __name__, url_prefix='')

import app.public.controllers

