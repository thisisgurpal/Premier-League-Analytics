/* Create position Ids */
DECLARE @tableName NVARCHAR(128) = N'[Premier League Scrape].[dbo].[position_id]';

IF OBJECT_ID(@tableName, 'U') IS NOT NULL
BEGIN
    -- Drop the table if it exists
    EXEC('DROP TABLE ' + @tableName);
END

-- Insert data into a new clean table
EXEC ('
WITH PositionsRanked AS (
    SELECT 
		[Position],
        ROW_NUMBER() OVER (ORDER BY [Position]) AS Id
    FROM [Premier League Scrape].[dbo].[player_stats_clean] 
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
')