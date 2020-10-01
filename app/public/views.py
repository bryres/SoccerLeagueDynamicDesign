from app.public import public_mod
from app.public.controllers import *
from datetime import datetime, timedelta
from flask import g, redirect, render_template, request, url_for, jsonify, flash

import collections

@public_mod.route('/')
def index():
    return render_template("public/index.html")

def shift_date_back_to_sunday (start_date):
    while start_date.weekday() != 6:
        start_date = start_date + timedelta(-1)
    return start_date

@public_mod.route('/schedule')
def schedule():
    # get date from query string, default to today is no date in the request
    start_date = request.args.get('start_date',  datetime.date(datetime.now()))

    sunday_date = shift_date_back_to_sunday (start_date)

    schedule_data = get_schedule_data (sunday_date)

    return render_template("public/schedule.html")
