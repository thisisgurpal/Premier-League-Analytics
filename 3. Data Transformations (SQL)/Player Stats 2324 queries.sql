/* Player Stats Queries */

/* Who currently in the Premier League Season 2023/24 does the most passes per match? */
SELECT
	[First Name],
	[Last Name],
	[Team Name],
	[Passes per Match]
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
WHERE [Team Id] IS NOT NULL AND [Passes per Match] IS NOT NULL
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

/* Which position has the tallest average height for players involved in the Premier League Season 2023/24? */
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
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
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
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
WHERE [Tackle Success] IS NOT NULL AND [Height] IS NOT NULL
) AS A
GROUP BY A.[Height Group]
ORDER BY [Average Tackle Success] desc

/* Reviewing player height and tackle success for players involved in the Premier League Season 2023/24? */
SELECT
	[Height],
	[Tackle Success]
FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
WHERE [Tackle Success] IS NOT NULL AND [Height] IS NOT NULL



