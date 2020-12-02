from app.db import execute, query_one, query


def get_teams() -> []:
    return query(statement='''select league_name, name as team_name, t.team_id
                            from team t, league l
                            where t.league_id = l.league_id
                            order by league_name, team_name''',
                 dictResults=True)


def get_fields() -> []:
    return query(statement='''select field_name, field_id
                            from field
                            order by field_name''',
                 dictResults=True)


def load_game(game_id) -> {}:
    return query_one(statement='''select game_id, home_team_id, away_team_id, field_id, 
                                    DATE_FORMAT(game_dt, '%%Y-%%m-%%d') as game_date,
                                    DATE_FORMAT(game_dt, '%%l:%%i %%p') as game_time,
                                    home_score, away_score 
                                    from game 
                                    where game_id = %s''',
                     vars=(game_id),
                     dictResults=True)


def modify_game(game_id, home_team_id, away_team_id, field_id, game_dt, game_time, home_score, away_score):
    dt_time = game_dt + " " + game_time

    execute(statement='''UPDATE game 
                        set home_team_id = %s, 
                        away_team_id = %s, 
                        field_id = %s, 
                        game_dt = %s, 
                        home_score = %s, 
                        away_score = %s
                        where game_id = %s''',
            vars=(home_team_id, away_team_id, field_id, dt_time, home_score, away_score, game_id))


def add_game(home_team_id, away_team_id, field_id, game_dt, game_time, home_score, away_score):
    dt_time = game_dt + " " + game_time

    execute(statement='''INSERT INTO game (home_team_id, away_team_id, field_id, game_dt, home_score, away_score) 
                         VALUES (%s, %s, %s, %s, %s, %s)''',
            vars=(home_team_id, away_team_id, field_id, dt_time, home_score, away_score))


def delete_game(game_id):
    execute(statement='delete from game where game_id = %s', vars=(game_id))


def get_schedule_data(sunday_date) -> []:
    return query(statement='''select home.name as home_team_name, away.name as away_team_name, 
                        home.team_id as home_team_id, away.team_id as away_team_id,
                        l.league_name, f.field_name,
                        DATE_FORMAT(game_dt, '%%b %%e (%%a)') as game_date,                                        
                        DATE_FORMAT(game_dt, '%%l:%%i %%p') as game_time,
                        g.home_score, g.away_score, g.game_id                                           
                        from league l, team home, team away, game g      
                        left join field f on g.field_id = f.field_id                               
                        where g.home_team_id = home.team_id
                        and g.away_team_id = away.team_id
                        and home.league_id = l.league_id
                        and g.game_dt >= %s
                        and g.game_dt < DATE_ADD(%s, INTERVAL 7 DAY)
                        order by league_name, game_dt, field_name''',
                 vars=[sunday_date,sunday_date],
                 dictResults=True)


def get_players_for_game(game_id) -> []:
    return query(statement='''select t.name as team_name, CONCAT(p.last_name, ', ', p.first_name) as player_name, minutes_played, p.player_id, g.game_id
                            from game g, team t, player p
                            left join player_game_time pgt on p.player_id = pgt.player_id
                            where (g.home_team_id = t.team_id or g.away_team_id = t.team_id)
                            and t.team_id = p.team_id
                            and g.game_id = %s  
                            order by team_name, player_name''',
                 vars=(game_id),
                 dictResults=True)


def add_update_player_minutes(game_id, player_id, minutes):
    execute(statement=
            '''INSERT INTO player_game_time(game_id, player_id, minutes_played)
            VALUES(%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            minutes_played = %s''', vars=(game_id, player_id, minutes, minutes))
