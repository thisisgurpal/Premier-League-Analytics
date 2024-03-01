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

# Webscraper class to scrape the data
class TeamStatsScraper:

    # Initialise data containers
    def __init__(self):
        self.team_stats = { 'team_stats': []}
        self.page_change = 0

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
    def locate_team_links(self, body, position):
        # Locate a tag for each team's overview page
        tr = body.find_element(By.CSS_SELECTOR, f'tr[data-position="{position}"]')
        td = tr.find_element(By.CSS_SELECTOR, 'td[class="league-table__team team"]')
        a = td.find_element(By.TAG_NAME, 'a')

        # Click and navigate to team overview page
        self.click_filter(a)
    
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
        self.page_change += 1

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
        # Locate body
        body = driver.find_element(By.CSS_SELECTOR, 'tbody[class="league-table__tbody isPL"]')

        # For each position in table
        for position in range(1,21):
            # Count page changes
            self.page_change = 0

            # Locate and click tag for team's overview page
            self.locate_team_links(body, position)

            # Allow page to load
            time.sleep(5)

            # Locate navigation bar tabs
            li = self.locate_nav_tabs(driver)

            # Click 'Stats' tab
            self.click_stats_tab(li)

            # Allow page to load
            time.sleep(5)

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
        
            # Allow page to load
            time.sleep(5)

            # Go back to leage table to move onto next team
            driver.execute_script(f'window.history.go(-{self.page_change})')

            # Allow page to load
            time.sleep(1)

    # Scapa team stats
    def scrape_data(self, season_text, url):
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
                self.get_team_stats(season_text, driver)
            except Exception as e:
                # Print error
                print("An error occurred get_team_stats:", str(e))

                # Pass
                pass
            
            # Return team stats data
            return self.team_stats
            
        except Exception as e:
            print("An error occurred:", str(e))
        
        finally:
            # Close the browser window
            driver.quit()

# Webscraper class to scrape the data
class PlayerStatsScraper:

    # Initialise data containers
    def __init__(self):
        self.player_stats = { 'player_stats': []}
        self.player_hrefs = []

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
        
    # Scroll to bottom of page
    def scroll_to_bottom(self, driver):
        # Get initial page height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2) 

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    # Get a list a player links
    def get_player_links(self, driver):
        # Locate elements
        div_table = driver.find_element(By.CSS_SELECTOR, 'div[class="table playerIndex player-listing"]')
        table = div_table.find_element(By.TAG_NAME, 'table')
        tbody = table.find_element(By.CSS_SELECTOR, 'tbody[class="dataContainer indexSection"]')

        # Locate player elements
        tr_players = tbody.find_elements(By.CSS_SELECTOR, 'tr[class="player"]')

        # Loop through player elements
        for tr_player in tr_players:
            # Locate player info elements
            td_elements = tr_player.find_elements(By.TAG_NAME, 'td')

            # Choose first player info element
            a = td_elements[0].find_element(By.TAG_NAME, 'a')

            # Get the player link
            player_href = a.get_attribute('href')

            # Append player link to player_hrefs
            self.player_hrefs.append(player_href)

    # Get player image
    def get_player_img(self, driver, dict_):
        try:
            # Locate elements
            player_container = driver.find_element(By.CSS_SELECTOR, 'div[class="wrapper playerContainer"]') 
            image_container = player_container.find_element(By.CSS_SELECTOR, 'div[class="imgContainer"]')
            image_img = image_container.find_element(By.TAG_NAME, 'img')

            # Get image url
            image_url = image_img.get_attribute('src')

            # Add image url to dict
            dict_['image_url'] = image_url

        except:
            pass

    # Get player name
    def get_player_name(self, driver, dict_):
        # Try and get first name
        try:
            # Locate elements
            div_first = driver.find_element(By.CSS_SELECTOR, 'div[class="player-header__name-first"]')

            # Get first name
            first_name = div_first.get_attribute('innerHTML').strip()

            # Append first name to dict
            dict_['first_name'] = first_name
        except:
            pass
        
        # Try and get last name
        try:
            # Locate elements
            div_last = driver.find_element(By.CSS_SELECTOR, 'div[class="player-header__name-last"]')

            # Get last name
            last_name = div_last.get_attribute('innerHTML').strip()

            # Append last name to dict
            dict_['last_name'] = last_name
        except:
            pass

    # Locate overview containers
    def locate_overview_containers(self, driver):
        # Locate elements
        player_side_widget = driver.find_element(By.CSS_SELECTOR, 'section[class="player-overview__side-widget"]')
        player_overview_containers = player_side_widget.find_elements(By.CSS_SELECTOR, 'div[class="player-overview__col"]')

        return player_overview_containers
    
    # Locate overview label
    def locate_overview_label(self, container):
        # Locate label container
        label_container = container.find_element(By.CSS_SELECTOR, 'div[class="player-overview__label"]')

        # Get label name
        label_name = label_container.get_attribute('innerHTML')

        return label_name

    # Get player nationality
    def get_player_nationality(self, driver, dict_):
        try:
            # Found boolean
            found = False

            # Locate elements
            player_overview_containers = self.locate_overview_containers(driver)

            # For player overview in overviews
            for player_overview_container in player_overview_containers:
                # Get label name
                label_name = self.locate_overview_label(player_overview_container)

                # If label 'Nationality'
                if label_name == 'Nationality':
                    # Found
                    found = True

                    # Locate container
                    nationality_container = player_overview_container.find_element(By.CSS_SELECTOR, 'div[class="player-overview__info"]')
                    nationality_span = nationality_container.find_element(By.CSS_SELECTOR, 'span[class="player-overview__player-country"]')

                    # Get nationality
                    nationality = nationality_span.get_attribute('innerHTML')

                    # Append player nationality name to dict
                    dict_[label_name] = nationality

                    # Locate container for flag
                    flag_span = nationality_container.find_element(By.CSS_SELECTOR, 'span[class="flag player-overview__flag"]')
                    img = flag_span.find_element(By.CSS_SELECTOR, 'img[class="player-overview__flag-icon"]')

                    # Get nationality
                    flag_url = img.get_attribute('src')

                    # Append player nationality name to dict
                    dict_['Flag'] = flag_url

                    # Break
                    break
            
            if found == False:
                # Append player nationality name to dict
                dict_['Nationality'] = ''
                dict_['Flag'] = ''

        except:
            pass

    # Get player position
    def get_player_position(self, driver, dict_):
        try:
            # Found boolean
            found = False

            # Locate elements
            player_overview_containers = self.locate_overview_containers(driver)

            # For player overview in overviews
            for player_overview_container in player_overview_containers:
                # Get label name
                label_name = self.locate_overview_label(player_overview_container)

                # If label 'Position'
                if label_name == 'Position':
                    # Found
                    found = True

                    # Locate container
                    position_container = player_overview_container.find_element(By.CSS_SELECTOR, 'div[class="player-overview__info"]')

                    # Get position
                    position_name = position_container.get_attribute('innerHTML')

                    # Append player position name to dict
                    dict_[label_name] = position_name

                    # Break
                    break

            if found == False:
                # Append player position name to dict
                dict_['Position'] = ''

        except:
            pass

    # Get player height
    def get_player_height(self, driver, dict_):
        try:
            # Found boolean
            found = False

            # Locate elements
            player_overview_containers = self.locate_overview_containers(driver)

            # For player overview in overviews
            for player_overview_container in player_overview_containers:
                # Get label name
                label_name = self.locate_overview_label(player_overview_container)

                # If label 'Position'
                if label_name == 'Height':
                    # Found
                    found = True

                    # Locate container
                    height_container = player_overview_container.find_element(By.CSS_SELECTOR, 'div[class="player-overview__info"]')

                    # Get height
                    height = height_container.get_attribute('innerHTML')

                    # Append player height name to dict
                    dict_[label_name] = height

                    # Break
                    break

            if found == False:
                # Append player height name to dict
                dict_['Height'] = ''

        except:
            pass

    # Get player date of birth
    def get_player_dob(self, driver, dict_):
        try:
            # Found
            found = False

            # Locate elements
            player_overview_containers = self.locate_overview_containers(driver)

            # For player overview in overviews
            for player_overview_container in player_overview_containers:
                # Get label name
                label_name = self.locate_overview_label(player_overview_container)

                # If label 'Position'
                if label_name == 'Date of Birth':
                    # Found
                    found = True

                    # Locate container
                    dob_container = player_overview_container.find_element(By.CSS_SELECTOR, 'div[class="player-overview__info"]')

                    # Get dob
                    dob = dob_container.get_attribute('innerHTML').strip()

                    # Append player dob name to dict
                    dict_[label_name] = dob

                    # Break
                    break
            
            if found == False:
                # Append player dob name to dict
                dict_['Date of Birth'] = ''

        except:
            pass

    # Get player appearances
    def get_player_appearances(self, driver, dict_):
        try:
            # Found boolean
            found = False

            # Locate elements
            div_pl_player = driver.find_element(By.CSS_SELECTOR, 'div[data-script="pl_player"]')
            player_overview_containers = div_pl_player.find_elements(By.CSS_SELECTOR, 'div[class="player-overview__col"]')

            # For player overview in overviews
            for player_overview_container in player_overview_containers:
                # Get label name
                label_name = self.locate_overview_label(player_overview_container)

                # If label 'Position'
                if label_name == 'Appearances':
                    # Found
                    found = True

                    # Locate container
                    appearances_container = player_overview_container.find_element(By.CSS_SELECTOR, 'div[class="player-overview__info"]')

                    # Get appearances
                    appearances = appearances_container.get_attribute('innerHTML')

                    # Append player appearances name to dict
                    dict_[label_name] = appearances

                    # Break
                    break

            if found == False:
                # Append player appearances name to dict
                dict_['Appearances'] = ''

        except:
            pass

    # Get player team name
    def get_player_team_name(self, driver, dict_):
        try:
            # Found boolean
            found = False

            # Locate elements
            player_overview_containers = self.locate_overview_containers(driver)

            # For player overview in overviews
            for player_overview_container in player_overview_containers:
                # Get label name
                label_name = self.locate_overview_label(player_overview_container)

                # If label 'Club'
                if label_name == 'Club':
                    # Found
                    found = True

                    # Get tag
                    a = player_overview_container.find_element(By.TAG_NAME, 'a')

                    # Get team name
                    team_name = a.get_attribute('innerHTML').split('<')[0].strip()

                    # Append player team name to dict
                    dict_[label_name] = team_name

                    # Break
                    break

            if found == False:
                # Append player appearances name to dict
                dict_['Club'] = ''

        except:
            pass

    # Get player details stats
    def get_player_detailed_stats(self, driver, dict_):
        try:
            # Locate elements
            app_span = driver.find_element(By.CSS_SELECTOR, 'span[data-stat="appearances"]')

            # Get value
            apps = app_span.get_attribute('innerHTML')

            # Append to dict_
            dict_['Appearances'] = apps

        except:
            pass

        try:
            # Locate elements
            ul = driver.find_element(By.CSS_SELECTOR, 'ul[class="player-stats__stats-wrapper"]')

            # Locate player stat high level containers
            li_containers = ul.find_elements(By.CSS_SELECTOR, 'li[class="player-stats__stat"]')

            # Loop through containers with stats
            for li in li_containers:
                # Locate elements with stats
                div_player_stats = li.find_element(By.CSS_SELECTOR, 'div[class="player-stats__stat-wrapper"]')
                div_stats = div_player_stats.find_elements(By.CSS_SELECTOR, 'div[class="player-stats__stat-value"]')

                # Loop through elements with stats
                for div_stat in div_stats:
                    # Get label name
                    label_name_html = div_stat.get_attribute('innerHTML')
                    label_name = label_name_html.split('<')[0].strip()

                    # Get value
                    span = div_stat.find_element(By.TAG_NAME, 'span')
                    value = span.get_attribute('innerHTML')

                    # Append to dict_
                    dict_[label_name] = value

        except:
            pass
    
    def click_season_for_stats(self, season_text, driver):
        season_dropdown_div = driver.find_element(By.CSS_SELECTOR, 'div[data-dropdown-block="compSeasons"]')
        season_dropdown_current_div = season_dropdown_div.find_element(By.CSS_SELECTOR, 'div[data-dropdown-current="compSeasons"]')
        season_dropdown_current_div.click()
        dropdownListContainer = season_dropdown_div.find_element(By.CSS_SELECTOR, 'div[class="dropdownListContainer"]')
        ul = dropdownListContainer.find_element(By.CSS_SELECTOR, 'ul[data-dropdown-list="compSeasons"]')
        li_elements = ul.find_elements(By.TAG_NAME, 'li')

        for li in li_elements:
            if li.get_attribute('innerHTML') == season_text:
                li.click()

    # Get player overview stats data
    def get_overview_player_stats(self, driver, dict_):
        # Get player name
        self.get_player_name( driver, dict_)

        # Get player team name
        self.get_player_team_name(driver, dict_)

        # Get player position
        self.get_player_position(driver, dict_)
        
        # Get player height
        self.get_player_height(driver, dict_)

        # Get player nationality
        self.get_player_nationality(driver, dict_)

        # Get player date of birth
        self.get_player_dob(driver, dict_)

        # Get player appearances
        # self.get_player_appearances(driver, dict_)

        # Get player image
        self.get_player_img(driver, dict_)
    
    # Click the 'Stats' tab in the nav
    def click_stats_tab(self, driver):
        try:
            # Locate stats li
            stats_ul = driver.find_element(By.CSS_SELECTOR, 'ul[class="tablist generic-tabs-nav__nav"]')
            stats_li = stats_ul.find_element(By.CSS_SELECTOR, 'li[data-nav-index="1"]')

            # Find stats link
            a = stats_li.find_element(By.TAG_NAME, 'a')

            # Click link
            a.click()

            # Allow page to load
            time.sleep(1)

            # Handle blockers
            self.handle_blockers(driver)

        except:
            pass

    # Get player stats
    def get_player_stats(self, season_text, driver):        
        # Create dict to save data
        dict_ = {}

        # Handle blockers
        self.handle_blockers(driver)

        # Allow page to load
        # time.sleep(3)

        # Get overview player stats and add to dict
        self.get_overview_player_stats(driver, dict_)

        # Click stats tab
        self.click_stats_tab(driver)

        # Allow page to load
        # time.sleep(3)

        # Filter 2023/24
        self.click_season_for_stats(season_text, driver)

        # Allow page to load
        time.sleep(3)

        # Get detailed player stats and add to dict
        self.get_player_detailed_stats(driver, dict_)
        
        # Append dict to 'team_stats'
        self.player_stats['player_stats'].append(dict_)
        # print(self.player_stats)

        # print(dict_)
            

    # Scapa team stats
    def scrape_data(season_text, self):
        # Initialise Selenium webdriver
        driver = webdriver.Chrome() 

        # Try open url
        try:
            # Loop through player links
            for index, player_href in enumerate(self.player_hrefs):
                if index == 0:
                    # self.go_to_player_link(player_href, driver)
                    driver.get(player_href)

                    time.sleep(6)
                elif (index % 50) == 0:
                    # Quit driver
                    driver.quit()
        
                    # Restart initialisation of Selenium webdriver
                    driver = webdriver.Chrome()

                    # self.go_to_player_link(player_href, driver)
                    driver.get(player_href)

                    time.sleep(6)

                else:
                    # self.go_to_player_link(player_href, driver)
                    driver.get(player_href)

                    time.sleep(3)
                    
                # Try get player stats
                try:
                    # Get player stats
                    self.get_player_stats(season_text, driver)

                    # Print to check progress
                    print('Completed: ', index, ' Total: ', len(self.player_hrefs))
            
                except Exception as e:
                    # Print error
                    print("An error occurred get_player_stats:", str(e))
                
            # Return player stats data
            return self.player_stats
            
        except Exception as e:
            print("An error occurred:", str(e))
        
        finally:
            # Close the browser window
            driver.quit()

    # Scapa team stats
    def get_links(self, url):
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

            # Try get player stats
            try:
                # Scroll to bottom of page for all links to load
                self.scroll_to_bottom(driver)

                # Get a list a player links
                self.get_player_links(driver)
            except Exception as e:
                # Print error
                print("An error occurred get_player_stats:", str(e))

                # Pass
                pass
            
        except Exception as e:
            print("An error occurred:", str(e))
        
        finally:
            # Close the browser window
            driver.quit()