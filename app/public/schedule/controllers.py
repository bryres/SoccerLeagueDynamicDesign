from datetime import datetime, timedelta, date

from flask import render_template, request, redirect, url_for, session

from app.public import public_mod
from app.public.schedule.models import *
import json

@public_mod.route('/game_add', methods=['GET', 'POST'])
@public_mod.route('/game_modify', methods=['GET', 'POST'])
def add_modify_game_controller():

    # Initially loading the pages
    if request.method == 'GET':
        rule = request.url_rule

        if 'game_add' in rule.rule:
            return render_template("schedule/game_add_modify.html", mode="Add",
                                   teams=get_teams(), fields=get_fields())
        else:
            game_id = request.args['game_id']
            return render_template("schedule/game_add_modify.html", mode="Modify",
                                   game=load_game(game_id),
                                   teams=get_teams(), fields=get_fields())


    # Saving the results of the pages
    else:
        mode = request.form['choice']
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

        if mode == 'Modify':
            modify_game(request.form['game_id'], home_team_id, away_team_id, field_id, game_dt, game_time, home_score, away_score)

        else:
            add_game(home_team_id, away_team_id, field_id, game_dt, game_time, home_score, away_score)

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

    # Converting the date to a string and assigning to the session.
    # Without the explicit conversion to a string, it wasn't working for some students.  It seemed to be
    # auto-converting to a string, but in a different format.
    session['start_date'] = start_date.strftime("%Y-%m-%d")

    return render_template("schedule/schedule.html", schedule_data=schedule_data, date_range=date_range_str, prior_week=prior_week, next_week=next_week)


@public_mod.route('/playing_time')
def show_playing_time():
    game_id = request.args['game_id']


    return render_template("schedule/player_time.html", game_id=game_id, players=get_players_for_game(game_id), teams=get_teams_for_game(game_id))


@public_mod.route('/player_minutes')
def ajax_player_minutes():
    game_id = request.args['game_id']
    player_id = request.args['player_id']
    minutes = request.args['minutes']

    if len(minutes) == 0:
        minutes = 0

    add_update_player_minutes(game_id, player_id, minutes)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@public_mod.route('/ajax_add_player')
def ajax_add_player():
    team_id = request.args['team_id']
    last_name = request.args['last_name']
    first_name = request.args['first_name']

    player_id = add_player(team_id, last_name, first_name)
    player = get_player(player_id)

    return json.dumps({'player_id': player_id,
                       'team_name': player['team_name'],
                       'player_name': player['player_name']}), 200, {'ContentType': 'application/json'}


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

