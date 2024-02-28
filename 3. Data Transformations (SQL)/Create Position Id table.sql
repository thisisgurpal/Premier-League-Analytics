/* Create position Ids */
WITH PositionsRanked AS (
    SELECT 
		[Position],
        ROW_NUMBER() OVER (ORDER BY [Position]) AS Id
    FROM [Premier League Scrape].[dbo].[player_stats_2324_clean] 
	WHERE [Position] IS NOT NULL
     GROUP BY 
        [Position]
)
SELECT 
    [Position],
    Id
INTO [Premier League Scrape].[dbo].[position_id]
FROM 
    PositionsRanked
ORDER BY 
    [Position];