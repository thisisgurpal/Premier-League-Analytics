# Premier League Team & Player Dashboards

This project is for **football lovers**. Football lovers who want to stay updated. Football lovers who want to know the stats. 

Is Rordi the top **passer per match**? 

Does Virgil Van Dijk have the best **tackle success** rate? 

What is the **shooting accuracy** of Erling Haaland? 

Which team gets the most **cards**? 

Click [here](https://public.tableau.com/app/profile/gurpalgohler/viz/PremierLeagueDashboard_17095666895140/PremierLeagueDashboard) to go to the live dashboard and get answers to all these questions, and more.


![Premier League Dashboard Tableau](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/619ea0ca-aabb-4ff3-bdef-269afd0539c1)

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Data Collection](#2-data-collection)
- [3. Data Cleaning](#3-data-cleaning)
- [4. Data Transformation](#4-data-transformation)
- [5. Dashboard building](#5-dashboard-building)
- [6. Future Conciderations](#6-future-conciderations)
- [7. Conclusion](#7-conclusion)

## 1. Introduction

I wanted to learn web scraping. I thought about certifications. I thought about text books. But no, I think the best way to learn is by doing. I chose a passion which is football. Scraped 2000+ lines of data, along with multiple attributes, from the Premier League website. Python, selenium and pandas were my weapons of choice. The cleaning and transformations were done using SQL. Then it was time to create the visualisations, where I used Tableau. The result is an interactive dashboard, updated weekly, showing the statistics you want to know about your favourite players and teams this season.

## 2. Data Collection

Collecting the data. This is where the idea for the project started. To learn about web scraping. I built python classes, containing multiple functions. These classes are for getting, table stats, team stats, and player stats from the Premier League website. To explain what I did, I will choose LeagueTableScraper() as an example from [league_table_class.py](https://github.com/thisisgurpal/Premier-League-Analytics/blob/master/1.%20Webscraping%20%26%20Data%20Collection%20(Python)/Weekly%20Collection/Webscrape%20Classes/league_table_class.py).

### 2.1 Imports

Firstly let's import the modules we need. We need 'webdriver' from selenium, to work with the website browser. 'By' from Selenium to locate html elements. The 'By' import uses different ways to locate these elements. the one's I've used are 'CSS_SELECTOR', 'TAG_NAME', 'ID' and 'CLASS_NAME'. Lastly the 'time' module. This is used to allow html elements to load, through delaying the execution of the next piece of code.

![Imports](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/cdaba14f-bc8d-43d2-b0ad-df9b215b1153)

### 2.2 Configuring the class

To configure the class, we give a name for it. Mine being 'LeagueTableScraper'. I then decided to store the data within the class, hence creating a dictionary (self.premier_league) that contains an element with an empty array ('premier_league': []) where the data can get appended. This will allow me to loop through pages, append the data, and then return what we have collected at the end.

![ConfiguringTheClass](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/630f2bb7-0364-40ca-9e96-a428c44cf32c)

### 2.3 The scraper function

I want to call only one function to scrape. To do all the scraping. That is my function called scrape_data(). This will take two parameters. One being the season (season_text) we want to scrape. The second being the initial url to open. 

![scrape_data](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/66f16693-9c48-480a-b143-37923ac0fcb2)

Let's break this down to get to know this function better.

#### 2.3a Start the chrome session

The first line of the function creates a variable called 'driver'. This variable starts my chrome browser session from the webdriver.

![StartChromeSession](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/3b9e9f8e-e0cb-4db9-b643-dc25b666b9d7)

#### 2.3b Try and get URL

Now we have our chrome driver. We want to try and go to the url passed into the function. To do this we use the 'get' method from the driver. I have placed this inside of a try block. If if fails for any reason, the except part will print the error. Finally after the try and except, we stop the chrome sesson using the 'quit' method.

![TryGetUrl](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/63b05139-263a-4a39-b34b-fd1003160d23)

#### 2.3c Handling blockers

At the moment we are just testing the url. I reviewed and paid close attention. We got pop ups. We got ads. To handle this I located the html elements and clicked on the closed buttons, which formed the function handle_blockers. This function needs to be run after we get the url. However we need the page to load before executing this function. So we use the time module. Now inside our try block, it looks like this.

![TryWithHandleBlocks](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/aafe07fd-7c4f-46cf-ad53-824fb9cab90a)

I found only two blockers that occur on the website. So within the handle_blockers function I have two try except blocks. For each, when the blocker is present, the try section locates the close button, and clicks it. When it's not present, the except section does a 'pass', it moves on.

![HandleBlockers](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/d684ad3f-f157-4ea0-8cf2-f2b0f4d7b4b1)

#### 2.3d Get the data

Now were at the points we want to start getting the data, and storing it for collection. To do this, I've creating a function called get_all_premier_leagues_data(). This function takes the 'season_text' to know which season to get data for. The second parameter it takes is the 'driver', to access page elements. So inside of the current try block and under the handle_blockers function we put another try block. This is to handle errors when getting the data. 

![GetData](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/b3b6a216-4621-4e3c-b831-b0a97eda6949)

Let's take a closer look at this function.

Firstly in the get_all_premier_leagues_data() function we need to get the seasons to filter. The open_season_dropdown() is a function I've written to find and open the season dropdown. The find_seasons() function returns a list of the seasons available.

![StartGetPremierLeaguesData](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/606ffebe-f453-4e4c-b60b-d4384c43b7e0)

Now we can loop through these seasons. This is where season_text is used. If the user gives season_text as 'All'. We collect league table data for all seasons going back to 1992. If they specify a season like '2012/13'. We only collect league table data for that season. 

The count is used when season_text is 'All'. It allows us to reopen the dropdown after the first one, as initially the dropdown has been opened before the loop.

So when season_text is 'All'. We loop through all the individual season filters, ignoring the 'All seasons' filter. We want the specific data for each season, not the sum of all seasons. After we click a season, we get the data and append it to our dictionary using another function, get_premier_league_data().

![season_text_all](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/d37c17d1-6fd7-462b-ad2c-488e25c7e324)

For season_text being an individual season like '2012/13'. We check if the season dropdown we are looping through is the same as '2012/13'. When that is true, the filter is clicked. The data is collected and appended using get_premier_league_data(). Finally we break out of the season loop, because we only wanted that one season.

![season_text_individual](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/55efc504-5045-4819-b781-2d967a8a241d)

So your now asking yourself. What's inside of get_premier_league_data(). We'll I'm here to tell you. 

Once we have clicked a season to filter, the league table is updated. Ready for us to collect stats. Essentially the function locates the body where the teams are located. Each team is within an element that uses their position in the league. As the premier league always has 20 positions, we can loop through each of these numbers. For each position, we get the element of the team in that position. this is done using the function locate_team_tags(). We can use these elements returned to get our data. Other than the team name and season, we use the get_team_info() function to retreive our information. Now that we have all the stats, it's time to append to our dictionary. Using append_data(). which take the parameters of the data points.

![get_data_pl](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/08429c6a-30d7-4c2f-b1a4-ebc8ad74a9f6)

The append function. It looks like this. Quite simple.

![append](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/7cfcb1b1-f666-4bf7-9ab8-2c8a106a75f8)

Lastly in the scrape_data() function, we return the data.

![return_data](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/6b54fa30-e6be-4efe-b8b8-066cbfea4669)

All that's left to do now is, initialise our class, and call our function. Allow the function to finish running, and boom. Our data is collected.

![boom](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/f62ee74c-d62e-47db-bfbb-0a17780ff420)

## 3. Data Cleaning

I could have cleaned the data in python. But where is the fun in that. Why not use SQL, and test my skills. Let's looks at the [Player Stats 2324 (Data Clean)](https://github.com/thisisgurpal/Premier-League-Analytics/blob/master/2.%20Data%20Cleaning%20(SQL)/Player%20Stats%202324%20(Data%20Clean).sql) file. This file is used to clean the player stats data after importing the data collected into SQL server. Now before running SQL code to clean this data and save it. We have to check if the cleaned file already exists, so that we can replace it, or create it. That looks like this, where our SELECT statment for cleaning goes within the '' in EXEC('').

![replace_playerstats_SQL](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/441fd7f7-70dc-4cda-a4b9-add3d03a0971)

The select statement for the cleaning. In this code we join new columns, replace values, amend values and specify data types. As an example look at Date_of_Birth. The values in the data are either '20/12/1995' or '20/12/1995 (28)' where 28 is the age. I just want the date. This calls for the CAST method. Which allows us to do a WHEN, THEN and ELSE statement (like an if, else statement). So within the WHEN, we check for '(' and get the index. If the index is greater than 0, the age is present. We use THEN to make the change. Take the substring of Date_of_Birth from index 1 to the index before '(' is present. Then CONVERT to the specified data type.

![player_stats_clean_SQL](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/eebc2038-bc23-46c9-b69b-b3f7278a65d6)

## 4. Data Transformation

Our data is nice and clean now. Ready for some transformations using SQL. You can find the transformation queries here - [Data Export Queries](https://github.com/thisisgurpal/Premier-League-Analytics/blob/master/4.%20Data%20Export%20from%20SQL/Data%20Export%20Queries.sql). These queries help summarise statistics to be used in the dashboard. Here is an example. 

Height (cm) vs Features query. This query needed a transformation of the data to allow for filtering in Tableau. Instead of having the data like this:

![HeightFeaturesQueryDataBefore](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/881d846e-623b-47be-ad01-e71908d2e362)

I wanted it like this:

![HeightFeaturesQueryDataAfter](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/8372b620-e0be-4930-9541-521ff35dede6)

To do that, this is the SQL query I wrote. As a side note. I found that when the Team is NULL, the player is no longer in the league. As you can see in the query too.

![HeightFeaturesQuery](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/8147de05-affc-4d1b-8654-b5383af9985d)

## 5. Dashboard building

Now I've got my data tranformations. The tables are exported. Uploaded to Tableau desktop. The main data table that everything goes through, for filtering purposes is 'Player_and_Team PL 2324.csv'. This table is a distict list of all players in the current Premier League season, with their teams and positons. The 'Team Stats PL 2324.csv' is going through 'Teams PL 2324.csv'. This is because the chart related to 'Team Stats PL 2324.csv' needs to go through a table of distinct teams. Which is 'Teams PL 2324.csv'.

![TableauRelationships](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/2027cd66-cad5-428d-a951-3bd28db49144)

I add the position, team and player columns from 'Player_and_Team PL 2324.csv' in this data to filter each chart. These columns are also added to the context of each chart, to enable the data to be fitlered by these columns before building the charts.

![ContectTableau](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/4d6543c3-5de6-476d-a20f-993894c5a47c)

After some trial and error. More filtering. More designing. It's finished. The dashboard has been built. Most of the charts can also be used as a filter too, so feel free to click away.

![Premier League Dashboard Tableau](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/bb4358bc-6317-462d-bfe6-025e1e4bd994)

## 6. Future Conciderations

Going forward, if it was to advance this dashboard. I would scrape not only players in the 2023/2024 season. But in every season in the premier league. This will allow the dashboard to contain players like, Cristiano Ronaldo and Gareth Bale. The comparison between players in different season would then be quite interesting to add and look into. How players have changed over the seasons. 

Another data source I would like to add is the history of injuries for the players. This would allow for some statistical calculations. Predicting the risk of injury for a player.

## 7. Conclusion

In conclusion, my journey into web scraping was a great learning experience. Instead of traditional methods like certifications or textbooks, I opted for a project. Driven by my passion for football. Using Python, Selenium, and Pandas, I collected over 2000 lines of data from the Premier League website. Cleaning and transforming the data was made easy with SQL. Then, with Tableau, I crafted an interactive dashboard showcasing insights into players and teams statistics. This project improved my technical skills, and enhanced my experience.
