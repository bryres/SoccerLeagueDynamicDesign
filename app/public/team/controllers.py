from flask import render_template, request

from app.public import public_mod
from app.public.team.models import *


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

    return render_template("public/../../templates/teams/team.html", team_info=team_info, team_schedule=team_schedule, results_str=record)

