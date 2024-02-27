/* Player Stats Queries */

/* Who currently in the Premier League Season 2023/24 does the most passes per match? */
SELECT
	[First Name],
	[Last Name],
	[Team Name],
	[Passes per Match]
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
WHERE [Team Id] IS NOT NULL
ORDER BY [Passes per Match] desc

/* Who currently in the Premier League Season 2023/24 has made the most apperances? */
SELECT
	[First Name],
	[Last Name],
	[Team Name],
	[Appearances]
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
WHERE [Team Id] IS NOT NULL
ORDER BY [Appearances] desc

/* Which team currently in the Premier League Season 2023/24 has the highest average player age? */
SELECT
	[Team Name],
	AVG(DATEDIFF(YEAR, [Date of Birth], GETDATE())) AS 'Average Age'
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
WHERE [Team Id] IS NOT NULL
GROUP BY [Team Name]
ORDER BY [Average Age] desc

/* Which player under 20 years of age currently in the Premier League Season 2023/24 has the highest appearances? */
SELECT * FROM
(
    SELECT
        [First Name],
        [Last Name],
        [Team Name],
        CAST(DATEDIFF(YEAR, [Date of Birth], GETDATE()) AS INT) AS 'Age',
        [Appearances]
    FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
    WHERE [Team Id] IS NOT NULL
) AS SubQuery
WHERE [Age] < 20
ORDER BY [Appearances] desc;

/* What is the average 'Height' by player 'Position' for players that have been in the Premier League Season 2023/24? */
SELECT
	[Position],
	AVG([Height]) AS 'Average Height'
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
WHERE Height IS NOT NULL
GROUP BY Position
ORDER BY [Average Height] desc

/* Which team has the tallest players currently in the Premier League Season 2023/24? */
SELECT
	[Team Name],
	AVG([Height]) AS 'Average Height'
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
WHERE Height IS NOT NULL AND [Team Id] IS NOT NULL
GROUP BY [Team Name]
ORDER BY [Average Height] desc

