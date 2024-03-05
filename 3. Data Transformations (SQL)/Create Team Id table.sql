/* Create Team Name Id table for 2023 and 2024 season */
DECLARE @tableName NVARCHAR(128) = N'[Premier League Scrape].[dbo].[team_2324_id]';

IF OBJECT_ID(@tableName, 'U') IS NOT NULL
BEGIN
    -- Drop the table if it exists
    EXEC('DROP TABLE ' + @tableName);
END

-- Insert data into a new clean table
EXEC ('
SELECT * 
INTO [Premier League Scrape].[dbo].[team_2324_id]
FROM (
SELECT 
    [Team Name],
    ROW_NUMBER() OVER (ORDER BY [Team Name]) AS Id
FROM 
    [Premier League Scrape].[dbo].[premier_league_tables_clean]
WHERE 
    [Season] = ''2023/24''
GROUP BY 
    [Team Name]
) AS A
')