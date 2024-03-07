# Premier League Team & Player Dashboards

This project is for **football lovers**. Football lovers who want to stay updated. Football lovers who want to know the stats. 

Is Rordi the top **passer per match**? 

Does Virgil Van Dijk have the best **tackle success** rate? 

What is the **shooting accuracy** of Erling Haaland? 

Which team gets the most **cards**? 

Click [here](https://public.tableau.com/app/profile/gurpalgohler/viz/PremierLeagueDashboard_17095666895140/PremierLeagueDashboard) to go to the live dashboard and get answers to all these questions, and more.


![Premier League Dashboard Tableau](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/619ea0ca-aabb-4ff3-bdef-269afd0539c1)

## Table of Contents
- [Introduction](#introduction)
- [Data Collection](#data-collection)
- [Data Cleaning](#data-cleaning)
- [Data Transformation](#data-transformation)
- [Dashboard building](#dashboard-building)
- [Future Conciderations](#future-conciderations)
- [Conclusion](#conclusion)

## Introduction

I wanted to learn webscraping. I thought about certifications. I thought about text books. But no, I reckon the best way to learn is by doing. I chose a passion which is football, and scraped 2000+ lines of data. Along with multiple attributes, from the Premier League website. Python, selenium and pandas were my weapons of choice. The data I collected was muddy. It needed a bath and make over, SQL was the detergent. Then I had to dress the data to tell the story, this is where tableau came to the rescue. The results is a well designed and interactive dashboard.

## Data Collection

Collecting the data. This is where the idea for the project started. To learn about web scraping. I built python classes, containing multiple functions. These classes are for getting, table stats, team stats, and player stats from the Premier League website. To explain what I did, I will choose LeagueTableScraper() as an example from [league_table_class.py](https://github.com/thisisgurpal/Premier-League-Analytics/blob/master/1.%20Webscraping%20%26%20Data%20Collection%20(Python)/Weekly%20Collection/Webscrape%20Classes/league_table_class.py).

Firstly let's import the modules we need. We need 'webdriver' from selenium, fto work with the website browser. 'By' from Selenium to locate html elements. The 'By' import uses different ways to locate these elements. the one's I've used are 'CSS_SELECTOR', 'TAG_NAME', 'ID' and 'CLASS_NAME'. Lastly the 'time' module. This is used to allow html elements to load, through delaying running the next piece of code.

![Imports](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/cdaba14f-bc8d-43d2-b0ad-df9b215b1153)

## Data Cleaning
## Data Transformation
## Dashboard building
## Future Conciderations
## Conclusion
