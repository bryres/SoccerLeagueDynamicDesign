from app.db import insert, insertmany, query_one, query, delete, update


def get_schedule_data(sunday_date) -> []:
    return query(statement='''select home.name as home_team_name, away.name as away_team_name, 
                        home.team_id as home_team_id, away.team_id as away_team_id,
                        l.league_name, f.field_name,
                        DATE_FORMAT(game_dt, '%%b %%e (%%a)') as game_date,                                        
                        DATE_FORMAT(game_dt, '%%l:%%i %%p') as game_time,
                        g.home_score, g.away_score                                           
                        from league l, game g, team home, team away, field f                                    
                        where g.home_team_id = home.team_id
                        and g.away_team_id = away.team_id
                        and home.league_id = l.league_id
                        and g.field_id = f.field_id
                        and g.game_dt >= %s
                        and g.game_dt < DATE_ADD(%s, INTERVAL 7 DAY)
                        order by league_name, game_dt, field_name''',
                    vars=[sunday_date,sunday_date],
                    dictResults=True)

