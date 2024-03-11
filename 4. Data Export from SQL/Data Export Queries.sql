/* Export queries for Dashboard */

/* Get team stats for all seasons of team's in the premier league 23/24 */
SELECT
	A.*,
	B.Points,
	B.[Goal Difference]
FROM (
SELECT 
	REPLACE(REPLACE([Team Name], 'AFC Bournemouth', 'Bournemouth'), 'Brighton and Hove Albion', 'Brighton & Hove Albion') AS 'Team',
	[Season],
    [Matches Played],
    [Wins],
    [Losses],
    [Goals],
    [Goals per Match],
    [Shots],
    [Shot on Target],
    [Shooting Accuracy],
    [Penalties Scored],
    [Big Chances Created],
    [Hit Woodwork],
    [Passes],
    [Passes per Match],
    [Pass Accuracy],
    [Crosses],
    [Cross Accuracy],
    [Clean Sheets],
    [Goals Conceded],
    [Goals Conceded per Match],
    [Saves],
    [Tackles],
    [Tackle Success],
    [Blocked Shots],
    [Interceptions],
    [Clearances],
    [Headed Clearance],
    [Aerial Battles Won],
    [Errors Leading to Goals],
    [Own Goals],
    [Yellow Cards],
    [Red Cards],
    [Fouls],
    [Offsides]	
FROM [Premier League Scrape].[dbo].[team_stats_clean]
) AS A
LEFT JOIN [Premier League Scrape].[dbo].premier_league_tables_clean AS B
ON A.Season = B.Season AND A.[Team] = B.[Team Name]
ORDER BY A.[Team]

/* Who in the Premier League Season 2023/24 scores the most goals? */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Goals]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Goals] IS NOT NULL
ORDER BY [Goals] desc

/* Who in the Premier League Season 2023/24 does the most passes per match? */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Passes per Match]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Passes per Match] IS NOT NULL
ORDER BY [Passes per Match] desc

/* Who in the Premier League Season 2023/24 has made the most apperances? */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Appearances]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Appearances] IS NOT NULL
ORDER BY [Appearances] desc

/* Reviewing player 'Height' with 'Tackle Success', 'Shooting Accuracy' and 'Cross Accuracy' for players involved in the Premier League Season 2023/24? */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Height] AS 'Height (cm)',
	[Tackle Success] AS 'Value',
	CAST([Tackles] AS VARCHAR(50)) + ' Tackles' AS 'Frequency',
	[Tackles] AS 'Frequency Value',
	'Tackle Success' AS 'Measure'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Tackle Success] IS NOT NULL 
AND [Height] IS NOT NULL
AND [Tackles] > 0

UNION ALL

SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
    [Height] AS 'Height (cm)',
    [Shooting Accuracy] AS 'Value',
	CAST([Shots] AS VARCHAR(50)) + ' Shots' AS 'Frequency',
	[Shots] AS 'Frequency Value',
    'Shooting Accuracy' AS 'Measure'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Shooting Accuracy] IS NOT NULL 
    AND [Height] IS NOT NULL
    AND [Shots] > 0

UNION ALL

SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
    [Height] AS 'Height (cm)',
    [Cross Accuracy] AS 'Value',
	CAST([Crosses] AS VARCHAR(50)) + ' Crosses' AS 'Frequency',
	[Crosses] AS 'Frequency Value',
    'Cross Accuracy' AS 'Measure'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Cross Accuracy] IS NOT NULL 
    AND [Height] IS NOT NULL
    AND [Crosses] > 0

/* Who in the Premier League Season 2023/24 makes the most assists? */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Assists]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Assists] IS NOT NULL
ORDER BY [Assists] desc

/* Create Team Name Id table for 2023 and 2024 season */
SELECT 
	[Team Name] as 'Team',
	[Id]
FROM [Premier League Scrape].[dbo].[team_2324_id]

/* Create position Ids */
SELECT
	*
FROM [Premier League Scrape].[dbo].[position_id]

/* Create player Ids */
SELECT
	[Player Name] AS 'Player',
	[Id]
FROM [Premier League Scrape].[dbo].[player_2324_id]

/* Player and Cards */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
    [Red Cards] AS 'Count',
    'Red Card' AS [Type]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Red Cards] IS NOT NULL

UNION ALL

SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
    [Yellow Cards] AS 'Count',
    'Yellow Card' AS [Type]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Yellow Cards] IS NOT NULL

/* Get all players with team and position */
SELECT * FROM
(
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
) AS A
WHERE 'Player' IS NOT NULL

/* Goals, Assists, Apearances, Passes union */
SELECT * FROM (
(
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Passes per Match] AS 'Value',
	'Passes per Match' AS 'Measure'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Passes per Match] IS NOT NULL)

UNION ALL

(SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Goals] AS 'Value',
	'Goals' AS 'Measure'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Goals] IS NOT NULL)

UNION ALL

(SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Appearances] AS 'Value',
	'Appearances' AS 'Measure'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Appearances] IS NOT NULL)

UNION ALL

(SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS 'Player',
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS 'Team',
	[Position],
	[Assists] AS 'Value',
	'Assists' AS 'Measure'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Assists] IS NOT NULL)
) a;

/* Losses, wins and draws */
SELECT
	[Team Name] AS 'Team',
	[Won] AS 'Value',
	'Won' AS 'Measure'
FROM [Premier League Scrape].[dbo].[premier_league_tables_clean]
WHERE [Won] IS NOT NULL AND [Season] = '2023/24'

UNION ALL

SELECT
	[Team Name] AS 'Team',
	[Lost] AS 'Value',
	'Lost' AS 'Measure'
FROM [Premier League Scrape].[dbo].[premier_league_tables_clean]
WHERE [Lost] IS NOT NULL AND [Season] = '2023/24'

UNION ALL

SELECT
	[Team Name] AS 'Team',
	[Drawn] AS 'Value',
	'Drawn' AS 'Measure'
FROM [Premier League Scrape].[dbo].[premier_league_tables_clean]
WHERE [Drawn] IS NOT NULL AND [Season] = '2023/24'