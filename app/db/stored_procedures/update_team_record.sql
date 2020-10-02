drop PROCEDURE `update_team_record`;
CREATE PROCEDURE `update_team_record`(IN `teamId` INT)
BEGIN

    update team
    set T = (select count(*)
            from game
            where (home_team_result = 'T' and home_team_id = teamId)
               or (away_team_result = 'T' and away_team_id = teamId)),
        W = (select count(*)
            from game
            where (home_team_result = 'W' and home_team_id = teamId)
               or (away_team_result = 'W' and away_team_id = teamId)),
        L = (select count(*)
            from game
            where (home_team_result = 'L' and home_team_id = teamId)
               or (away_team_result = 'L' and away_team_id = teamId))
    where team_id = teamId;
END