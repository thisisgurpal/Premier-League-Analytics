from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Webscraper class to scrape the data
class LeagueTableScraper:

    # Initialise data containers
    def __init__(self):
        self.premier_league = { 'premier_league': []}

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
    
    # Locate tags for team
    def locate_team_tags(self, body, position):
        # Locate elements
        tr = body.find_element(By.CSS_SELECTOR, f'tr[data-position="{position}"]')
        td = tr.find_elements(By.TAG_NAME, 'td')

        return tr, td
    
    # Locate body element
    def locate_body(self, driver):
         # Locate body
        body = driver.find_element(By.CSS_SELECTOR, 'tbody[class="league-table__tbody isPL"]') 

        return body
    
    # Get team information
    def get_team_info(self, td):
        count = 1 # Data tags do not have classes so I use the count and order of the tags to determine what the value means

        # Loop through each tag
        for value in td:
            # Get the text in the tag
            innerHTML = value.get_attribute('innerHTML') 

            # Check if it's a digit
            if innerHTML.lstrip('-').isdigit(): 
                if count == 1:
                    played = innerHTML # How many games have been played
                elif count == 2:
                    won = innerHTML # How many games have been won
                elif count == 3:
                    drawn = innerHTML # How many games have been drawn
                elif count == 4:
                    lost = innerHTML # How many games have been lost
                elif count == 5:
                    gf = innerHTML # How many goals the team has scored
                elif count == 6:
                    ga = innerHTML # How many goals have been conceded
                elif count == 7:
                    gd = innerHTML # The goal difference between goals scored and goals conceded
                elif count == 8:
                    points = innerHTML # Number of league points
                else:
                    break
                
                count += 1 # Increase count to handle tag order

        return played, won, drawn, lost, gf, ga, gd, points

    # Append data
    def append_data(self, season, team_name, position, played, won, drawn, lost, gf, ga, gd, points):
        # Append data to 'premier_league' using a dictionary
        self.premier_league['premier_league'].append(
            {
                    'season': season, # Season
                    'team_name': team_name, # Team name
                    'position': position, # Position in league
                    'played': played, # Games played
                    'won': won, # Games won
                    'drawn': drawn, # Games drawn
                    'lost': lost, # Games lost
                    'gf': gf, # Goals scored
                    'ga': ga, # Goals conceded
                    'gd': gd, # Goal difference
                    'points': points, # Team league points
            }
        )

    # Open season filter dropdown
    def open_season_dropdown(self, driver):
        # Locate and open season filter dropdown
        dropdown = driver.find_element(By.CSS_SELECTOR, 'div[data-dropdown-block="compSeasons"]') 
        dropdown.click() # Click season dropdown

        return dropdown

    # Find all the options in the season filter dropdown
    def find_seasons(self, dropdown):
        # Locate all season items in list
        seasons_div = dropdown.find_element(By.CSS_SELECTOR, 'div[class="dropdownListContainer"]')
        season_ul = seasons_div.find_element(By.CSS_SELECTOR, 'ul[class="dropdownList"]')
        seasons_li = season_ul.find_elements(By.TAG_NAME, 'li')

        return seasons_li

    # Function to get a single premier league table data
    def get_premier_league_data(self, driver, season):
        # Locate body
        body = self.locate_body(driver)

        # Loop through 20 league positions
        for position in range(1,21):
            # Locate elements
            tr, td = self.locate_team_tags(body, position)

            # Get team name
            team_name = tr.get_attribute('data-filtered-table-row-name')

            # Get team info
            played, won, drawn, lost, gf, ga, gd, points = self.get_team_info(td)

            # Append data
            self.append_data(season, team_name, position, played, won, drawn, lost, gf, ga, gd, points)

    # Get the premier league data for all seasons
    def get_all_premier_leagues_data(self, season_text, driver):
        
        # Allow page to load
        time.sleep(5) 

        # Locate and open season filter dropdown
        dropdown = self.open_season_dropdown(driver)

        # Allow dropdown to load
        time.sleep(1) 

        # Locate all season items in list
        seasons_li = self.find_seasons(dropdown)

        count = 1  # Create a count in order to decide when to open the dropdown

        # Loop through each season filter
        for season_li in seasons_li:
            if season_text == 'All':
                # Do not open the dropdown when count is 1 as it's already open
                # Open dropdown
                if count > 1:
                    # Locate and open season filter dropdown
                    dropdown = self.open_season_dropdown(driver)

                    # Allow dropdown to load
                    time.sleep(1) 

                # Only click filter for individual seasons and not 'All Seasons'
                if (season_li.get_attribute('data-option-name') != 'All Seasons'):
                    # Click season and filter table
                    season_li.click() 

                    # Allow league table to load
                    time.sleep(10) 

                    # Get season text
                    season = season_li.get_attribute('data-option-name') 

                    # Get premier league data for season
                    self.get_premier_league_data(driver, season) 

                    count += 1 # Increment count

                # If season filter is 'All Seasons' keep count as 1
                else:
                    count = count
            elif (season_li.get_attribute('data-option-name') == season_text):
                # Click season and filter table
                season_li.click() 

                # Allow league table to load
                time.sleep(10) 

                # Get season text
                season = season_li.get_attribute('data-option-name') 

                # Get premier league data for season
                self.get_premier_league_data(driver, season) 
        
                break
    

    # Function to scrape all premier league tables from all seasons
    def scrape_data(self, season_text, url):
        # Initialise Selenium webdriver
        driver = webdriver.Chrome() 

        # Try to open url
        try:
            driver.get(url) # Load the webpage
            
            # Allow page load
            time.sleep(2)

            # Handle ad blockers
            self.handle_blockers(driver) 

            # Allow page load
            time.sleep(2)

            # Try to get data
            try:
                # Get the premier league data for all seasons
                self.get_all_premier_leagues_data(season_text, driver)  

            except Exception as e:
                # Print error
                print("An error occurred get_premier_league:", str(e)) 

                # Pass error and move on
                pass 
            
            # Return data for premier league data for all seasons
            return self.premier_league 
            
        except Exception as e:
            # Print error
            print("An error occurred:", str(e))
        
        finally:
            # Close the browser window
            driver.quit() 