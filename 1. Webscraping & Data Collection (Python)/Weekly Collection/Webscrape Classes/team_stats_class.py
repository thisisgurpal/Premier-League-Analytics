from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Webscraper class to scrape the data
class TeamStatsScraper:

    # Initialise data containers
    def __init__(self):
        self.team_stats = { 'team_stats': []}
        self.team_links = []
        self.team_missed_hrefs = []

    # Function to handle add blockers
    def handle_blockers(self, driver):
        # Try to handle blocker
        try:
            # Locate and close blocker 
            accept = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept.click()
        except:
            pass

        # Try to handle blocker
        try:
            # Locate and close blocker
            accept = driver.find_element(By.ID, "advertClose")
            accept.click()
        except:
            pass
        
    # Locate <a> tags for team
    def get_team_links(self, driver):
        # Locate body
        body = driver.find_element(By.CSS_SELECTOR, 'tbody[class="league-table__tbody isPL"]')

        for position in range(1,21):
            # Locate a tag for each team's overview page
            tr = body.find_element(By.CSS_SELECTOR, f'tr[data-position="{position}"]')
            td = tr.find_element(By.CSS_SELECTOR, 'td[class="league-table__team team"]')
            a = td.find_element(By.TAG_NAME, 'a')
            href = a.get_attribute('href')

            # Append to array
            self.team_links.append(href)
    
    # Locate the nav element and it's tabs
    def locate_nav_tabs(self, driver):
        # Locate navigation bar tabs
        nav = driver.find_element(By.CSS_SELECTOR, 'nav[class="club-navigation wrapper"]')
        ul = nav.find_element(By.CSS_SELECTOR, 'ul[class="tablist club-navigation__nav"]')
        li = ul.find_elements(By.TAG_NAME, 'li')

        return li
    
    # Click the 'Stats' tab in the nav
    def click_stats_tab(self, li):
        # Loop through navigation tab names
        for item in li:
            # Find link for tab
            a = item.find_element(By.TAG_NAME, 'a')

            # Find link for 'Stats' page
            if a.get_attribute('data-text') == 'Stats':
                # Click 'Stats' tab
                self.click_filter(a)

                # Found 'Stats' tab so break loop
                break

    # Open seasons filter dropdown
    def open_seasons_dropdown(self, driver):
        # Locate and open season filter dropdown
        dropdown = driver.find_element(By.CSS_SELECTOR, 'div[data-dropdown-block="compSeasons"]') 
        dropdown.click() # Click season dropdown

        return dropdown
    
    # Locate the options for the season dropdown filter
    def locate_seasons(self, dropdown):
        # Locate all season items in list
        seasons_div = dropdown.find_element(By.CSS_SELECTOR, 'div[class="dropdownListContainer"]')
        season_ul = seasons_div.find_element(By.CSS_SELECTOR, 'ul[class="dropdownList"]')
        seasons_li = season_ul.find_elements(By.TAG_NAME, 'li')

        return seasons_li

    # Click to change page
    def click_filter(self, tag):
        tag.click() 

    # Get top level stats value
    def get_top_level_stats_value(self, container):
        container_ = container.find_element(By.CSS_SELECTOR, 'div[class="all-stats__top-stat"]')
        span = container_.find_element(By.TAG_NAME, 'span')
        value = span.get_attribute('innerHTML')

        return value
    
    # Get regurlar stats value
    def get_regular_stats_value(self, div_stat):
        stat_span = div_stat.find_element(By.CSS_SELECTOR, 'span[class="all-stats__regular-stat"]')
        stat_container = stat_span.find_element(By.TAG_NAME, 'span')
        value = stat_container.get_attribute('innerHTML')

        return value

    # Get top level stats
    def get_top_level_stats(self, driver, dict_):
        # Locate elements
        div_stats_wrapper = driver.find_element(By.CSS_SELECTOR, 'div[class="all-stats wrapper"]')
        div_all_stats = div_stats_wrapper.find_element(By.CSS_SELECTOR, 'div[data-widget="all-stats"]')
        stats_top_list = div_all_stats.find_element(By.CSS_SELECTOR, 'div[class="all-stats__top-list"]')

        # Locate stats containers
        stats_top_containers = stats_top_list.find_elements(By.CSS_SELECTOR, 'div[class="all-stats__top-stat-container"]')

        # Loop through containers and get values
        for container in stats_top_containers:
            # Get innerHTML for stats name
            stats_title_container = container.find_element(By.CSS_SELECTOR, 'div[class="all-stats__top-stat-name"]')
            innerHTML = stats_title_container.get_attribute('innerHTML')
            if innerHTML == 'Matches played':
                # Add value to dict
                dict_[innerHTML] = self.get_top_level_stats_value(container)
            elif innerHTML == 'Wins':
                # Add value to dict
                dict_[innerHTML] = self.get_top_level_stats_value(container)
            elif innerHTML == 'Losses':
                # Add value to dict
                dict_[innerHTML] = self.get_top_level_stats_value(container)

    # Get regular stats
    def get_regular_stats(self, driver, dict_):
        # Locate elements
        main_stats_ul = driver.find_element(By.CSS_SELECTOR, 'ul[class="all-stats__regular-list block-list-4 block-list-2-m"]')

        # Locate list of tags high level (Attact, Defence...)
        main_stats_li = main_stats_ul.find_elements(By.TAG_NAME, 'li')

        # Loop through highlevel tags
        for li in main_stats_li:
            # Locate elements
            div_li = li.find_element(By.CSS_SELECTOR, 'div[class="all-stats__list-container"]')

            # Locate stats containers
            div_stats = div_li.find_elements(By.CSS_SELECTOR, 'div[class="all-stats__regular-stat-container"]')

            # Loop through stats containers and find values
            for div_stat in div_stats:
                # Get innerHTML for stats name
                span = div_stat.find_element(By.CSS_SELECTOR, 'span[class="all-stats__regular-stat-name"]')
                innerHTML = span.get_attribute('innerHTML')
                
                # Add value to dict
                dict_[innerHTML] = self.get_regular_stats_value(div_stat)
            
    # Get season value
    def get_season(self, season_li, dict_):
        # Get season text
        season = season_li.get_attribute('data-option-name') 

        # Add value to dict
        dict_['Season'] = season

    # Get team name
    def get_team_name(self, driver, dict_):
        # Locate element
        header_container = driver.find_element(By.CSS_SELECTOR, 'header[data-widget="club-header"]')
        header_div = header_container.find_element(By.CSS_SELECTOR, 'div[class="club-header__text-content"]')
        header_h2 = header_div.find_element(By.TAG_NAME, 'h2')

        # Get innerHTML for team name
        innerHTML = header_h2.get_attribute('innerHTML')

        # Add value to dict
        dict_['Team name'] = innerHTML

    # Get stats data for team name, season and all other stats
    def get_stats_data(self, driver, dict_, season_li):
        # Get team name
        self.get_team_name(driver, dict_)

        # Get season text
        self.get_season(season_li, dict_)

        # Get top level stats
        self.get_top_level_stats(driver, dict_)

        # Get regular stats
        self.get_regular_stats(driver, dict_)

    # Function to get team stats
    def get_team_stats(self, season_text, driver):
        # Handle add blockers
        self.handle_blockers(driver)

        # Locate navigation bar tabs
        li = self.locate_nav_tabs(driver)

        # Click 'Stats' tab
        self.click_stats_tab(li)

        # Allow page to load
        time.sleep(3)

        # Handle add blockers
        self.handle_blockers(driver)

        # Locate and open season filter dropdown
        dropdown = self.open_seasons_dropdown(driver)

        # Allow dropdown to load
        time.sleep(1) 

        # Locate all season items in list
        seasons_li = self.locate_seasons(dropdown)

        count = 1  # Create a count in order to decide when to open the dropdown

        # Loop through each season filter
        for season_li in seasons_li:
            if season_text == 'All':
                # Do not open the dropdown when count is 1 as it's already open
                # Open dropdown
                if count > 1:
                    # Locate and open season filter dropdown
                    dropdown = self.open_seasons_dropdown(driver)

                    # Allow dropdown to load
                    time.sleep(1) 

                # Only click filter for individual seasons and not 'All Seasons'
                if (season_li.get_attribute('data-option-name') != 'All Seasons'):
                    # Click season and filter table
                    self.click_filter(season_li)

                    # Allow league table to load
                    time.sleep(4) 

                    # Create empty dict
                    dict_ = {}

                    # Get stats and information and add to dict
                    self.get_stats_data(driver, dict_, season_li)
                    
                    # Append dict to 'team_stats'
                    self.team_stats['team_stats'].append(dict_)

                    count += 1 # Increment count

                # If season filter is 'All Seasons' keep count as 1
                else:
                    count = count
            else:
                # Only click filter for individual seasons and not 'All Seasons'
                if (season_li.get_attribute('data-option-name') == season_text):
                    # Click season and filter table
                    self.click_filter(season_li)

                    # Allow league table to load
                    time.sleep(4) 

                    # Create empty dict
                    dict_ = {}

                    # Get stats and information and add to dict
                    self.get_stats_data(driver, dict_, season_li)
                    
                    # Append dict to 'team_stats'
                    self.team_stats['team_stats'].append(dict_)

                    break
    
    # Return missed hrefs
    def return_missed_hrefs(self):
        return self.team_missed_hrefs

    # Scapa team stats
    def scrape_data(self, team_links, season_text, isMissedRun):
        # Initialise Selenium webdriver
        driver = webdriver.Chrome() 

        if isMissedRun == True:
            print(team_links)
        
        # Try open url
        try:
            # Loop through player links
            for index, team_href in enumerate(team_links):
                if index == 0:
                    # self.go_to_player_link(player_href, driver)
                    driver.get(team_href)

                    time.sleep(6)
                elif (index % 50) == 0:
                    # Quit driver
                    driver.quit()
        
                    # Restart initialisation of Selenium webdriver
                    driver = webdriver.Chrome()

                    # self.go_to_player_link(player_href, driver)
                    driver.get(team_href)

                    time.sleep(6)

                else:
                    # self.go_to_player_link(player_href, driver)
                    driver.get(team_href)

                    time.sleep(3)

                max_attempts = 10
                attempt = 1

                while attempt <= max_attempts:
                    # Try get player stats
                    try:
                        # Get team stats
                        self.get_team_stats(season_text, driver)

                        # Print to check progress
                        print('Completed: ', index, ' Total: ', len(team_links))

                        break
                
                    except Exception as e:
                        # Print error
                        print(f"Attempt {attempt}, An error occurred at {index} for {team_links[index]}")
                        attempt += 1
                        driver.get(team_links)
                else:
                    if isMissedRun == False:
                        self.team_missed_hrefs.append(team_links)
                    print("Max attempts reached without success.")
            
            # Return team stats data
            return self.team_stats
            
        except Exception as e:
            print("An error occurred:", str(e))
        
        finally:
            # Close the browser window
            driver.quit()

# Scapa team stats
    def scrape_links(self, url):
        # Initialise Selenium webdriver
        driver = webdriver.Chrome() 
        
        # Try open url
        try:
            # Load the webpage
            driver.get(url)

            # Allow page load
            time.sleep(10)

            # Handle add blockers
            self.handle_blockers(driver)

            # Allow page load
            time.sleep(5)

            # Try get team stats
            try:
                # Get team stats
                self.get_team_links(driver)
            except Exception as e:
                # Print error
                print("An error occurred get_team_stats:", str(e))

                # Pass
                pass
            
            # Return team stats data
            return self.team_links
            
        except Exception as e:
            print("An error occurred:", str(e))
        
        finally:
            # Close the browser window
            driver.quit()