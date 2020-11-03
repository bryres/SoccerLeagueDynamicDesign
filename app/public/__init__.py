from flask import Blueprint

public_mod = Blueprint('public', __name__, url_prefix='')

import app.public.controllers
import app.public.schedule.controllers
import app.public.standings.controllers
import app.public.team.controllers

