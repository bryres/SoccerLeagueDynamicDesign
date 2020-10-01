from app.db import insert, insertmany, query_one, query, delete, update

def get_schedule_data(sunday_date):

    results = query(statement='''select home.name as home_team, away.name as away_team, l.league_name, f.field_name,  
                        DATE_FORMAT(game_dt, '%b %d (%a)') as game_date,                                        
                        DATE_FORMAT(game_dt, '%h:%i %p') as game_time                                           
                        from league l, game g, team home, team away, field f                                    
                        where g.home_team_id = home.team_id
                        and g.away_team_id = away.team_id
                        and home.league_id = l.league_id
                        and g.field_id = f.field_id
                        order by league_name, game_dt''',
                     vars=None,
                    dictResults=True)

    games = []

    for row in results:
        games.append(row)

    return games
