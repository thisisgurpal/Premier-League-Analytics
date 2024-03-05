/* Add data types and clean Premier League Table data */
/* Add data types and clean data */
DECLARE @tableName NVARCHAR(128) = N'[Premier League Scrape].[dbo].[premier_league_tables_clean]';

IF OBJECT_ID(@tableName, 'U') IS NOT NULL
BEGIN
    -- Drop the table if it exists
    EXEC('DROP TABLE ' + @tableName);
END

-- Insert data into a new clean table
EXEC ('
SELECT 
	CAST([season] AS VARCHAR(50)) AS ''Season'',
    CAST([team_name] AS VARCHAR(255)) AS ''Team Name'',
    CAST([position] AS INT) AS ''Position'',
    CAST([played] AS INT) AS ''Played'',
    CAST([won] as INT) AS ''Won'',
    CAST([drawn] as INT) AS ''Drawn'',
    CAST([lost] AS INT) AS ''Lost'',
    CAST([gf] AS INT) AS ''Goals For'',
    CAST([ga] AS INT) AS ''Goals Against'',
    CAST([gd] AS INT) AS ''Goal Difference'',
    CAST([points] AS INT) AS ''Points''
INTO [Premier League Scrape].[dbo].[premier_league_tables_clean]
FROM [Premier League Scrape].[dbo].[premier_league_tables_raw]
')