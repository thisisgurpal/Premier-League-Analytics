/* Player Stats Queries */

/* Get team stats for all seasons of team's in the premier league 23/24 */
SELECT
	A.*,
	B.Points,
	B.[Goal Difference]
FROM (
SELECT 
	REPLACE(REPLACE([Team Name], 'AFC Bournemouth', 'Bournemouth'), 'Brighton and Hove Albion', 'Brighton & Hove Albion') AS [Team Name],
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
ON A.Season = B.Season AND A.[Team Name] = B.[Team Name]
ORDER BY A.[Team Name]

/* Who in the Premier League Season 2023/24 scores the most goals? */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
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
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
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
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	[Position],
	[Appearances]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Appearances] IS NOT NULL
ORDER BY [Appearances] desc

/* Which team in the Premier League Season 2023/24 has the highest average player age? */
SELECT
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	AVG(DATEDIFF(YEAR, [Date of Birth], GETDATE())) AS 'Average Age'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Date of Birth] IS NOT NULL
GROUP BY [Team Name]
ORDER BY [Average Age] desc

/* Which player under 20 years of age in the Premier League Season 2023/24 has the highest appearances? */
SELECT * FROM
(
    SELECT
        CASE
			WHEN [First Name] IS NULL THEN
				[Last Name]
			ELSE
				[First Name] + ' ' + [Last Name]
		END AS [Player Name],
        CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
        CAST(DATEDIFF(YEAR, [Date of Birth], GETDATE()) AS INT) AS 'Age',
        [Appearances]
    FROM [Premier League Scrape].[dbo].[player_stats_clean]
    WHERE [Date of Birth] IS NOT NULL
) AS SubQuery
WHERE [Age] < 20
ORDER BY [Appearances] desc;

/* Which position has the tallest average height for players involved in the Premier League Season 2023/24? */
SELECT
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	[Position],
	AVG([Height]) AS 'Average Height',
	COUNT([Height]) AS 'Count'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE Height IS NOT NULL AND [Position] IS NOT NULL
GROUP BY [Team Name], [Position]
ORDER BY [Average Height] desc

/* Which team has the tallest players in the Premier League Season 2023/24? */
SELECT
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	AVG([Height]) AS 'Average Height'
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE Height IS NOT NULL
GROUP BY [Team Name]
ORDER BY [Average Height] desc

/* Do taller players make more tackles? */
SELECT
	A.[Height Group],
	AVG(A.[Tackles]) as 'Average Tackles'
FROM (
SELECT
	CASE 
        WHEN [Height] < 155 THEN
			'Less than 155'
		WHEN [Height] >= 155 AND [Height] < 160 THEN 
            '155 - 159'
        WHEN [Height] >= 160 AND [Height] < 165 THEN 
            '160 - 164'
		WHEN [Height] >= 165 AND [Height] < 170 THEN 
            '165 - 169'
		WHEN [Height] >= 170 AND [Height] < 175 THEN 
            '170 - 174'
		WHEN [Height] >= 175 AND [Height] < 180 THEN 
            '175 - 179'
		WHEN [Height] >= 180 AND [Height] < 185 THEN 
            '180 - 184'
		WHEN [Height] >= 185 AND [Height] < 190 THEN 
            '185 - 189'
		WHEN [Height] >= 190 AND [Height] < 195 THEN 
            '190 - 194'
		WHEN [Height] >= 195 AND [Height] < 200 THEN 
            '195 - 199'
		WHEN [Height] >= 200 THEN 
            'More than 200'
	END AS 'Height Group',
	[Tackles]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Tackles] IS NOT NULL AND [Height] IS NOT NULL
) AS A
GROUP BY A.[Height Group]
ORDER BY [Average Tackles] desc

/* Do taller players make better tackles? */
SELECT
	A.[Height Group],
	AVG(A.[Tackle Success]) as 'Average Tackle Success'
FROM (
SELECT
	CASE 
        WHEN [Height] < 155 THEN
			'Less than 155'
		WHEN [Height] >= 155 AND [Height] < 160 THEN 
            '155 - 159'
        WHEN [Height] >= 160 AND [Height] < 165 THEN 
            '160 - 164'
		WHEN [Height] >= 165 AND [Height] < 170 THEN 
            '165 - 169'
		WHEN [Height] >= 170 AND [Height] < 175 THEN 
            '170 - 174'
		WHEN [Height] >= 175 AND [Height] < 180 THEN 
            '175 - 179'
		WHEN [Height] >= 180 AND [Height] < 185 THEN 
            '180 - 184'
		WHEN [Height] >= 185 AND [Height] < 190 THEN 
            '185 - 189'
		WHEN [Height] >= 190 AND [Height] < 195 THEN 
            '190 - 194'
		WHEN [Height] >= 195 AND [Height] < 200 THEN 
            '195 - 199'
		WHEN [Height] >= 200 THEN 
            'More than 200'
	END AS 'Height Group',
	[Tackle Success]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Tackle Success] IS NOT NULL AND [Height] IS NOT NULL
) AS A
GROUP BY A.[Height Group]
ORDER BY [Average Tackle Success] desc

/* Reviewing player height and tackle success for players involved in the Premier League Season 2023/24? */
SELECT
	[Height],
	[Tackle Success]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Tackle Success] IS NOT NULL 
AND [Height] IS NOT NULL
AND [Tackles] > 0

/* Reviewing player height and cross accuracy for players involved in the Premier League Season 2023/24? */
SELECT
	[Height],
	[Cross Accuracy]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Cross Accuracy] IS NOT NULL 
AND [Height] IS NOT NULL
AND [Crosses] > 0

/* Reviewing player height and shooting accuracy for players involved in the Premier League Season 2023/24? */
SELECT
	[Height],
	[Shooting Accuracy]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Shooting Accuracy] IS NOT NULL 
AND [Height] IS NOT NULL
AND [Shots] > 0

/* Reviewing player 'Height' with 'Tackle Success', 'Shooting Accuracy' and 'Cross Accuracy' for players involved in the Premier League Season 2023/24? */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	[Position],
	[Height],
	[Tackle Success],
	CAST([Tackles] AS VARCHAR(50)) + ' Tackles' AS 'Frequency',
	'Tackle Success' AS [Type]
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
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	[Position],
    [Height],
    [Shooting Accuracy],
	CAST([Shots] AS VARCHAR(50)) + ' Shots' AS 'Frequency',
    'Shooting Accuracy' AS [Type]
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
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	[Position],
    [Height],
    [Cross Accuracy],
	CAST([Crosses] AS VARCHAR(50)) + ' Crosses' AS 'Frequency',
    'Cross Accuracy' AS [Type]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Cross Accuracy] IS NOT NULL 
    AND [Height] IS NOT NULL
    AND [Crosses] > 0

/* Get all players with team and position */
SELECT * FROM
(
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	[Position]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
) AS A
WHERE [Player Name] IS NOT NULL

/* Which position get's more Cards? */
SELECT * FROM
(
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	[Position],
	[Red Cards],
	[Yellow Cards]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
) AS A
WHERE [Player Name] IS NOT NULL

/* Who in the Premier League Season 2023/24 makes the most assists? */
SELECT
	CASE
		WHEN [First Name] IS NULL THEN
			[Last Name]
		ELSE
			[First Name] + ' ' + [Last Name]
	END AS [Player Name],
	CASE
		WHEN [Team Id] IS NULL THEN
			'No longer in league'
		ELSE
			[Team Name]
	END AS [Team Name],
	[Position],
	[Assists]
FROM [Premier League Scrape].[dbo].[player_stats_clean]
WHERE [Assists] IS NOT NULL
ORDER BY [Assists] desc

	






