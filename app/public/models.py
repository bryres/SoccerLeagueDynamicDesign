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


def get_team_info(team_id):
    return query_one(statement='''select league_name, name as team_name, coach_first_name, coach_last_name, 
                                        coach_email 
                        from league l, team t 
                        left join coach c on t.coach_id = c.coach_id
                        where t.league_id = l.league_id
                        and t.team_id = %s''',
                    vars=[team_id],
                    dictResults=True)



def get_team_schedule(team_id):
    return query(statement='''select 'Home' as HomeAway, opp.name as opponent_team_name,  opp.team_id as opponent_team_id, 
                           IF(ISNULL(g.away_score),'',CONCAT(g.home_score,'-',g.away_score)) as score,       
                           home_team_result as result,          
                            DATE_FORMAT(game_dt, '%%b %%e (%%a)') as game_date, DATE_FORMAT(game_dt, '%%l:%%i %%p') as game_time, game_dt, 
                           l.league_name, f.field_name
                           from league l, game g, team opp, field f                                    
                           where g.away_team_id = opp.team_id
                           and g.home_team_id = %s
                            and opp.league_id = l.league_id                           
                           and g.field_id = f.field_id
                           
                           UNION
                           
                           select 'Away' as HomeAway, opp.name as opponent_team_name,  opp.team_id as opponent_team_id, 
                           IF(ISNULL(g.away_score),'',CONCAT(g.away_score,'-',g.home_score)) as score,       
                           away_team_result as result,          
                            DATE_FORMAT(game_dt, '%%b %%e (%%a)') as game_date, DATE_FORMAT(game_dt, '%%l:%%i %%p') as game_time, game_dt,
                           l.league_name, f.field_name
                           from league l, game g, team opp, field f                                    
                           where g.home_team_id = opp.team_id
                           and g.away_team_id = %s
                            and opp.league_id = l.league_id                           
                           and g.field_id = f.field_id
                                                      
                           order by game_dt, field_name''',
                    vars=[team_id, team_id],
                    dictResults=True)

def get_league_rankings():
    return query(statement='''select l.league_name, l.league_id, t.team_id, t.name as team_name, 
                                W, L, T, (3*W + 1*T) as points 
                           from league l, team t
                           where l.league_id = t.league_id 
                           order by league_name, points desc''',
                 dictResults=True)
