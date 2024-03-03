/* Add data types and clean data */
SELECT 
	PS.*, 
	TID.Id AS 'Team Id'
INTO [Premier League Scrape].[dbo].[player_stats_2324_clean]
FROM
(
SELECT 
	CAST([first_name] AS VARCHAR(255)) AS 'First Name',
	CAST([last_name] AS VARCHAR(255)) AS 'Last Name',
	-- COALESCE handles when NULL the player is not in the league and U19 teams
	CAST(REPLACE(REPLACE([Club], 'amp;', ''), 'U19', '') AS VARCHAR(255)) AS 'Team Name',
	CAST([Position] AS VARCHAR(50)) AS 'Position',
	-- Remove 'cm' from Height
	CAST(SUBSTRING([Height], 1, CHARINDEX('cm', [Height]) - 1) AS INT) AS 'Height',
	CAST([Nationality] AS VARCHAR(100)) AS 'Nationality',
	CAST([Flag] AS VARCHAR(MAX)) AS 'Flag URL',
	-- CASE e.g. to remove age '(20)' from string '26/02/2024 (20)'
	CASE 
        WHEN CHARINDEX(' (', [Date_of_Birth]) > 0 THEN 
            -- If '(' is found
            CONVERT(DATE, SUBSTRING([Date_of_Birth], 1, CHARINDEX(' (', [Date_of_Birth]) - 1), 103)
        ELSE 
            -- If '(' is not found
			CONVERT(DATE, [Date_of_Birth], 103)
	END AS 'Date of Birth',
	CAST(REPLACE([Appearances], ',', '') AS INT) AS 'Appearances',
	CAST([image_url] AS VARCHAR(MAX)) AS 'Player Image URL',
	CAST(REPLACE([Clean_sheets], ',', '') AS INT) AS 'Clean Sheets',
	CAST(REPLACE([Goals_Conceded], ',', '') AS INT) AS 'Goals Conceded',
	CAST(REPLACE([Tackles], ',', '') AS INT) AS 'Tackles',
	CAST(CAST(REPLACE([Tackle_success], '%', '') AS DECIMAL(6, 2))/100 AS DECIMAL(3, 2)) AS 'Tackle Success',
	CAST(REPLACE([Last_man_tackles], ',', '') AS INT) AS 'Last Man Tackles',
	CAST(REPLACE([Blocked_shots], ',', '') AS INT) AS 'Blocked Shots',
	CAST(REPLACE([Interceptions], ',', '') AS INT) AS 'Interceptions',
	CAST(REPLACE([Clearances], ',', '') AS INT) AS 'Clearances',
	CAST(REPLACE([Headed_Clearance], ',', '') AS INT) AS 'Headed Clearance',
	CAST(REPLACE([Clearances_off_line], ',', '') AS INT) AS 'Clearance off Line',
	CAST(REPLACE([Recoveries], ',', '') AS INT) AS 'Recoveries',
	CAST(REPLACE([Duels_won], ',', '') AS INT) AS 'Duels Won',
	CAST(REPLACE([Duels_lost], ',', '') AS INT) AS 'Duels Lost',
	CAST(REPLACE([Successful_50_50s], ',', '') AS INT) AS 'Successful 50 50s',
	CAST(REPLACE([Aerial_battles_won], ',', '') AS INT) AS 'Aerial Battles Won',
	CAST(REPLACE([Aerial_battles_lost], ',', '') AS INT) AS 'Aerial Battles Lost',
	CAST(REPLACE([Own_goals], ',', '') AS INT) AS 'Own Goals',
	CAST(REPLACE([Errors_leading_to_goal], ',', '') AS INT) AS 'Errors Leading to Goals',
	CAST(REPLACE([Assists], ',', '') AS INT) AS 'Assists',
	CAST(REPLACE([Passes], ',', '') AS INT) AS 'Passes',
	CAST([Passes_per_match] AS DECIMAL(5, 2)) AS 'Passes per Match',
	CAST(REPLACE([Big_Chances_Created], ',', '') AS INT) AS 'Big Chances Created',
	CAST(REPLACE([Crosses], ',', '') AS INT) AS 'Crosses',
	CAST(CAST(REPLACE([Cross_accuracy], '%', '') AS DECIMAL(6, 2))/100 AS DECIMAL(3,2)) AS 'Cross Accuracy',
	CAST(REPLACE([Through_balls], ',', '') AS INT) AS 'Through Balls',
	CAST(REPLACE([Accurate_long_balls], ',', '') AS INT) AS 'Accurate Long Balls',
	CAST(REPLACE([Yellow_cards], ',', '') AS INT) AS 'Yellow Cards',
	CAST(REPLACE([Red_cards], ',', '') AS INT) AS 'Red Cards',
	CAST(REPLACE([Fouls], ',', '') AS INT) AS 'Fouls',
	CAST(REPLACE([Offsides], ',', '') AS INT) AS 'Offsides',
	CAST(REPLACE([Goals], ',', '') AS INT) AS 'Goals',
	CAST(REPLACE([Headed_goals], ',', '') AS INT) AS 'Headed Goals',
	CAST(REPLACE([Goals_with_right_foot], ',', '') AS INT) AS 'Right Foot Goals',
	CAST(REPLACE([Goals_with_left_foot], ',', '') AS INT) AS 'Left Foot Goals',
	CAST(REPLACE([Hit_woodwork], ',', '') AS INT) AS 'Hit Woodwork',
	CAST([Goals_per_match] AS DECIMAL(4, 2)) AS 'Goals per Match',
	CAST(REPLACE([Penalties_scored], ',', '') AS INT) AS 'Penalties Scored',
	CAST(REPLACE([Freekicks_scored], ',', '') AS INT) AS 'Freekicks Scored',
	CAST(REPLACE([Shots], ',', '') AS INT) AS 'Shots',
	CAST(REPLACE([Shots_on_target], ',', '') AS INT) AS 'Shots on Target',
	CAST(CAST(REPLACE([Shooting_accuracy], '%', '') AS DECIMAL(6, 2))/100 AS DECIMAL(3,2)) AS 'Shooting Accuracy',
	CAST(REPLACE([Big_chances_missed], ',', '') AS INT) AS 'Big Chances Missed',
	CAST(REPLACE([Saves], ',', '') AS INT) AS 'Saves',
	CAST(REPLACE([Penalties_Saved], ',', '') AS INT) AS 'Penalties Saved',
	CAST(REPLACE([Punches], ',', '') AS INT) AS 'Punched',
	CAST(REPLACE([High_Claims], ',', '') AS INT) AS 'High Claims',
	CAST(REPLACE([Catches], ',', '') AS INT) AS 'Catches',
	CAST(REPLACE([Sweeper_clearances], ',', '') AS INT) AS 'Sweeper Clearances',
	CAST(REPLACE([Throw_outs], ',', '') AS INT) AS 'Throw Outs',
	CAST(REPLACE([Goal_Kicks], ',', '') AS INT) AS 'Goal Kicks'
FROM [Premier League Scrape].[dbo].[player_stats_2324_raw]
) AS PS
LEFT JOIN [Premier League Scrape].[dbo].[team_2324_id] AS TID
ON PS.[Team Name] = TID.[Team Name]






  