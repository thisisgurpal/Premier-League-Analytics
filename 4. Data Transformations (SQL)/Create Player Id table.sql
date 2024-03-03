/* Create player Ids */
WITH PlayersRanked AS (
    SELECT 
		[Player Name],
        ROW_NUMBER() OVER (ORDER BY [Player Name]) AS Id
    FROM 
		(SELECT
			CASE
				WHEN [First Name] IS NULL THEN
					[Last Name]
				ELSE
					[First Name] + ' ' + [Last Name]
			END AS [Player Name]
		FROM [Premier League Scrape].[dbo].[player_stats_2324_clean]
		) AS A
	WHERE [Player Name] IS NOT NULL
     GROUP BY 
        [Player Name]
)
SELECT 
    [Player Name],
    Id
INTO [Premier League Scrape].[dbo].[player_2324_id]
FROM 
    PlayersRanked
ORDER BY 
    [Player Name];