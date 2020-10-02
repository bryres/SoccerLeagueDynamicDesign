DROP TRIGGER IF EXISTS `GAME_BEFORE_INSERT`;
CREATE TRIGGER `GAME_BEFORE_INSERT` BEFORE INSERT ON `game` FOR EACH ROW
 BEGIN
     if (new.home_score is not null AND new.away_score is not null) then
         if (new.home_score > new.away_score) then
             set new.home_team_result := 'W';
             set new.away_team_result := 'L';
         elseif (new.home_score < new.away_score) then
             set new.home_team_result := 'L';
             set new.away_team_result := 'W';
         else
             set new.home_team_result := 'T';
             set new.away_team_result := 'T';
         end if;
     end if;
 END;

DROP TRIGGER IF EXISTS `GAME_BEFORE_UPDATE`;
CREATE TRIGGER `GAME_BEFORE_UPDATE` BEFORE UPDATE ON `game` FOR EACH ROW
 BEGIN
     if (new.home_score is not null AND new.away_score is not null) then
         if (new.home_score > new.away_score) then
             set new.home_team_result := 'W';
             set new.away_team_result := 'L';
         elseif (new.home_score < new.away_score) then
             set new.home_team_result := 'L';
             set new.away_team_result := 'W';
         else
             set new.home_team_result := 'T';
             set new.away_team_result := 'T';
         end if;
     end if;
 END;


DROP TRIGGER IF EXISTS `GAME_AFTER_INSERT`;
CREATE TRIGGER `GAME_AFTER_INSERT` AFTER INSERT ON `game` FOR EACH ROW
 BEGIN
	 call update_team_record (new.home_team_id);
	 call update_team_record (new.away_team_id);
 END;

DROP TRIGGER IF EXISTS `GAME_AFTER_UPDATE`;
CREATE TRIGGER `GAME_AFTER_UPDATE` AFTER UPDATE ON `game` FOR EACH ROW
 BEGIN

     # Recal for the home teams.  Only recalc for the
     # old home team if it is different from the new home team.
     call update_team_record (new.home_team_id);
     if (new.home_team_id <> old.home_team_id) then
         call update_team_record (old.home_team_id);
     end if;

     # Recal for the away teams.  Only recalc for the
     # old away team if it is different from the new away team.
	 call update_team_record (new.away_team_id);
     if (new.away_team_id <> old.away_team_id) then
         call update_team_record (old.away_team_id);
     end if;
 END;

DROP TRIGGER IF EXISTS `GAME_AFTER_DELETE`;
CREATE TRIGGER `GAME_AFTER_DELETE` AFTER DELETE ON `game` FOR EACH ROW
 BEGIN
	 call update_team_record (old.home_team_id);
	 call update_team_record (old.away_team_id);
 END;
