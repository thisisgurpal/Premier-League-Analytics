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

I wanted to learn webscraping. I thought about certifications. I thought about text books. But no, I reckon the best way to learn is by doing. I chose a passion which is football, and scraped 2000+ lines of data. Along with multiple attributes, from the Premier League website. Python, selenium and pandas were my weapons of choice. The data I collected was muddy. It needed a bath and make over, SQL was the detergent. Then I had to dress the data to tell the story, this is where tableau came to the rescue. The results is a well designed and interactive dashboard.

## 2. Data Collection

Collecting the data. This is where the idea for the project started. To learn about web scraping. I built python classes, containing multiple functions. These classes are for getting, table stats, team stats, and player stats from the Premier League website. To explain what I did, I will choose LeagueTableScraper() as an example from [league_table_class.py](https://github.com/thisisgurpal/Premier-League-Analytics/blob/master/1.%20Webscraping%20%26%20Data%20Collection%20(Python)/Weekly%20Collection/Webscrape%20Classes/league_table_class.py).

### 2.1 Imports

Firstly let's import the modules we need. We need 'webdriver' from selenium, to work with the website browser. 'By' from Selenium to locate html elements. The 'By' import uses different ways to locate these elements. the one's I've used are 'CSS_SELECTOR', 'TAG_NAME', 'ID' and 'CLASS_NAME'. Lastly the 'time' module. This is used to allow html elements to load, through delaying the execution of the next piece of code.

![Imports](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/cdaba14f-bc8d-43d2-b0ad-df9b215b1153)

### 2.2 Configuring the class

To configure the class, we give a name for it. Mine being 'LeagueTableScraper'. I then decided to store the data within the class, hence creating a dictionary (self.premier_league) that contains an element with an empty array ('premier_league': []) where the data can get appended. This will allow me to loop through pages, append the data, and then return what we have collected at the end.

![ConfiguringTheClass](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/630f2bb7-0364-40ca-9e96-a428c44cf32c)

### 2.3 Building the scrape function

![scrape_data](https://github.com/thisisgurpal/Premier-League-Analytics/assets/97416784/7dcb7c14-fe9a-4929-b0a4-7efc716855e1)

#### 2.3a Handling blockers'

When I did the inital webscrapes, I got errors. It wasn't working. The reason was pop ups and ads. To handle this I located the html element and clicked on the closed button, which formed the function handle_blockers.

## 3. Data Cleaning
## 4. Data Transformation
## 5. Dashboard building
## 6. Future Conciderations
## 7. Conclusion
