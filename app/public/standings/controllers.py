from flask import render_template, request

from app.public import public_mod
from app.public.standings.models import *


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

