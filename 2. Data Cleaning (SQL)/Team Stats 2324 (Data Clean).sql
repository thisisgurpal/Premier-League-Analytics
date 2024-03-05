/* Add data types and clean Team Stats data */
/* Add data types and clean data */
DECLARE @tableName NVARCHAR(128) = N'[Premier League Scrape].[dbo].[team_stats_clean]';

IF OBJECT_ID(@tableName, 'U') IS NOT NULL
BEGIN
    -- Drop the table if it exists
    EXEC('DROP TABLE ' + @tableName);
END

-- Insert data into a new clean table
EXEC ('
SELECT 
	CAST([Team_name] AS VARCHAR(255)) AS ''Team Name'',
    CAST([Season] AS VARCHAR(50)) AS ''Season'',
    CAST(REPLACE([Matches_played], '','', '''') AS INT) AS ''Matches Played'',
    CAST(REPLACE([Wins], '','', '''') AS INT) AS ''Wins'',
    CAST(REPLACE([Losses], '','', '''') AS INT) AS ''Losses'',
    CAST(REPLACE([Goals], '','', '''') AS INT) AS ''Goals'',
    CAST([Goals_per_match] AS DECIMAL(4, 2)) AS ''Goals per Match'',
    CAST(REPLACE([Shots], '','', '''') AS INT) AS ''Shots'',
    CAST(REPLACE([Shots_on_target], '','', '''') AS INT) AS ''Shot on Target'',
	-- Remove ''%'' and divide by 100
    CAST(CAST(REPLACE([Shooting_accuracy], ''%'', '''') AS DECIMAl(5, 2))/100 AS DECIMAL(3, 2)) AS ''Shooting Accuracy'',
    CAST(REPLACE([Penalties_scored], '','', '''') AS INT) AS ''Penalties Scored'',
    CAST(REPLACE([Big_Chances_Created], '','', '''') AS INT) AS ''Big Chances Created'',
    CAST(REPLACE([Hit_woodwork], '','', '''') AS INT) AS ''Hit Woodwork'',
    CAST(REPLACE([Passes], '','', '''') AS INT) AS ''Passes'',
    CAST([Passes_per_match] AS DECIMAL(6, 2)) AS ''Passes per Match'',
	-- Remove ''%'' and divide by 100
	CAST(CAST(REPLACE([Pass_accuracy], ''%'', '''') AS DECIMAl(5, 2))/100 AS DECIMAL(3, 2)) AS ''Pass Accuracy'',
    CAST(REPLACE([Crosses], '','', '''') AS INT) AS ''Crosses'',
	-- Remove ''%'' and divide by 100
	CAST(CAST(REPLACE([Cross_accuracy], ''%'', '''') AS DECIMAl(5, 2))/100 AS DECIMAL(3, 2)) AS ''Cross Accuracy'',
    CAST(REPLACE([Clean_sheets], '','', '''') AS INT) AS ''Clean Sheets'',
    CAST(REPLACE([Goals_Conceded], '','', '''') AS INT) AS ''Goals Conceded'',
    CAST([Goals_conceded_per_match] AS DECIMAL(4, 2)) AS ''Goals Conceded per Match'',
    CAST(REPLACE([Saves], '','', '''') AS INT) AS ''Saves'',
    CAST(REPLACE([Tackles], '','', '''') AS INT) AS ''Tackles'',
	-- Remove ''%'' and divide by 100
	CAST(CAST(REPLACE([Tackle_success], ''%'', '''') AS DECIMAl(5, 2))/100 AS DECIMAL(3, 2)) AS ''Tackle Success'',
    CAST(REPLACE([Blocked_shots], '','', '''') AS INT) AS ''Blocked Shots'',
    CAST(REPLACE([Interceptions], '','', '''') AS INT) AS ''Interceptions'',
    CAST(REPLACE([Clearances], '','', '''') AS INT) AS ''Clearances'',
    CAST(REPLACE([Headed_Clearance], '','', '''') AS INT) AS ''Headed Clearance'',
    CAST(REPLACE([Aerial_Battles_Duels_Won], '','', '''') AS INT) AS ''Aerial Battles Won'',
    CAST(REPLACE([Errors_leading_to_goal], '','', '''') AS INT) AS ''Errors Leading to Goals'',
    CAST(REPLACE([Own_goals], '','', '''') AS INT) AS ''Own Goals'',
    CAST(REPLACE([Yellow_cards], '','', '''') AS INT) AS ''Yellow Cards'',
    CAST(REPLACE([Red_cards], '','', '''') AS INT) AS ''Red Cards'',
    CAST(REPLACE([Fouls], '','', '''') AS INT) AS ''Fouls'',
    CAST(REPLACE([Offsides], '','', '''') AS INT) AS ''Offsides''
INTO [Premier League Scrape].[dbo].[team_stats_clean]
FROM [Premier League Scrape].[dbo].[team_stats_raw]
')