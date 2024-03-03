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
FROM [Premier League Scrape].[dbo].[team_stats_2324_clean]
) AS A
LEFT JOIN [Premier League Scrape].[dbo].premier_league_tables_clean AS B
ON A.Season = B.Season AND A.[Team Name] = B.[Team Name]
ORDER BY A.[Team Name]

