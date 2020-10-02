from datetime import datetime, timedelta, date

from flask import render_template, request

from app.public import public_mod
from app.public.models import *


@public_mod.route('/')
def index():
    return render_template("public/index.html")


@public_mod.route('/schedule')
def show_schedule_page():
    # get date from query string, default to today is no date in the request
    start_date = request.args.get('start_date',  datetime.date(datetime.now()))

    # if the date was a "get" argument, convert it to a date object.
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    shifted_start_date = shift_date_back_to_saturday(start_date)
    date_range_str = get_date_range_str(shifted_start_date)

    schedule_data = get_schedule_data(shifted_start_date)
    prior_week = (start_date - timedelta(days=7)).strftime("%Y-%m-%d")
    next_week = (start_date + timedelta(days=7)).strftime("%Y-%m-%d")

    return render_template("public/schedule.html", schedule_data=schedule_data, date_range=date_range_str, prior_week=prior_week, next_week=next_week)


@public_mod.route('/team')
def show_team_page():
    team_id = request.args.get('team_id')
    team_info = get_team_info(team_id)
    team_schedule = get_team_schedule(team_id)

    results = {"W":0, "L":0, "T":0}
    for game in team_schedule:
        r = game["result"]
        if r in ("W", "L", "T"):
            results[r] = results[r] + 1

    record = str(results["W"]) + "W-" + str(results["L"]) + "L-" + str(results["T"]) + "T"

    return render_template("public/team.html", team_info=team_info, team_schedule=team_schedule, results_str=record)


@public_mod.route('/standings')
def show_standings_page():
    rankings = get_league_rankings()
    current_league_id = ''
    current_league = ''

    #
    # rankings_by_league will be a list of dictionaries.  The outer list is by league.
    # The dictionary has the team_list for the league along with the league_name.
    #
    rankings_by_league = []
    for team in rankings:
        # Create a new list and append a new dictionary entry whenever we reach a new league
        if team['league_id'] != current_league_id:
            current_league_id = team['league_id']
            current_league = []
            rankings_by_league.append({'team_list': current_league, 'league_name': team['league_name']})

        # append the current team to the league list
        current_league.append(team)

    return render_template("public/standings.html", rankings=rankings_by_league)


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

