from datetime import datetime, timedelta, date

from flask import render_template, request, redirect, url_for, session

from app.public import public_mod
from app.public.schedule.models import *

@public_mod.route('/game_add', methods=['GET', 'POST'])
def add_game_controller():

    # GET -- draw the modify page.
    if request.method == 'GET':
        return render_template("schedule/game_add.html", teams=get_teams(), fields=get_fields())

    # POST -- update the game
    else:
        home_team_id = request.form['home_team_id']
        away_team_id = request.form['away_team_id']
        field_id = request.form['field_id'] or None
        game_dt = request.form['game_dt']
        game_time = request.form['game_time']
        home_score = request.form['home_score'] or None
        away_score = request.form['away_score'] or None

        # convert from 12 hour clock to 24 hour
        in_time = datetime.strptime(game_time, "%I:%M %p")
        game_time = datetime.strftime(in_time, "%H:%M")

        if home_team_id and away_team_id:
            add_game(home_team_id, away_team_id, field_id, game_dt, game_time, home_score, away_score)

        return redirect(url_for('public.show_schedule_page'))



@public_mod.route('/game_modify', methods=['GET', 'POST'])
def modify_game_controller():
    # GET -- draw the modify page.
    if request.method == 'GET':
        game_id = request.args['game_id']
        return render_template("schedule/game_add_modify.html", mode="modify", game=load_game(game_id), teams=get_teams(), fields=get_fields())

    # POST -- modify the game
    else:
        game_id = request.form['game_id']
        home_team_id = request.form['home_team_id']
        away_team_id = request.form['away_team_id']
        field_id = request.form['field_id'] or None
        game_dt = request.form['game_dt']
        game_time = request.form['game_time']
        home_score = request.form['home_score'] or None
        away_score = request.form['away_score'] or None

        # convert from 12 hour clock to 24 hour
        in_time = datetime.strptime(game_time, "%I:%M %p")
        game_time = datetime.strftime(in_time, "%H:%M")

        modify_game(game_id, home_team_id, away_team_id, field_id, game_dt, game_time, home_score, away_score)

        return redirect(url_for('public.show_schedule_page'))


@public_mod.route('/game_delete', methods=['GET'])
def delete_game_controller():
    game_id = request.args['game_id']
    delete_game(game_id)
    return redirect(url_for('public.show_schedule_page'))


@public_mod.route('/schedule')
def show_schedule_page():
    # get date from query string.  If no value, pull from session (last time on this page).
    # If this is the first time the page is loading, default to today.
    start_date = request.args.get('start_date',
                                session.get('start_date',
                                    datetime.date(datetime.now())))

    # if the date was a "get" argument, convert it to a date object.
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    shifted_start_date = shift_date_back_to_saturday(start_date)
    date_range_str = get_date_range_str(shifted_start_date)

    schedule_data = get_schedule_data(shifted_start_date)
    prior_week = (start_date - timedelta(days=7)).strftime("%Y-%m-%d")
    next_week = (start_date + timedelta(days=7)).strftime("%Y-%m-%d")

    session['start_date'] = start_date

    return render_template("schedule/schedule.html", schedule_data=schedule_data, date_range=date_range_str, prior_week=prior_week, next_week=next_week)


def shift_date_back_to_saturday (start_date : date) -> date:
    """ Takes the passed date and returns the nearest preceding Saturday.  (If start_date
    is already a Saturday, the original date is returned. """
    w = start_date.weekday()

    # For Monday, w = 0;  For Sunday, w = 6.  Use this to calculate shift.
    shift = (w + 2) % 7

    return start_date - timedelta(days=shift)


def get_date_range_str (start_date : date) -> str:
    """ Returns a string  in the format May 30 - June 5 where the
    start date is first date in the competition week.  The second date will be 6
    days later, the last day in the competition week.  """
    end_date = start_date + timedelta(days=6)

    first_day_str = start_date.strftime("%b %e")
    last_day_str = end_date.strftime("%b %e")

    return first_day_str + "-" + last_day_str
