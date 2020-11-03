from app.db import query_one, query

def get_league_rankings():
    return query(statement='''select l.league_name, l.league_id, t.team_id, t.name as team_name, 
                                W, L, T, (3*W + 1*T) as points 
                           from league l, team t
                           where l.league_id = t.league_id 
                           order by league_name, points desc''',
                 dictResults=True)
