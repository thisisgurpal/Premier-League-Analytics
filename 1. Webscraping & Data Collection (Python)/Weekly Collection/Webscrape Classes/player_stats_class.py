from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Webscraper class to scrape the data
class PlayerStatsScraper:

    # Initialise data containers
    def __init__(self):
        self.player_stats = { 'player_stats': []}
        self.player_hrefs = []
        self.player_missed_hrefs = []

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

        time.sleep(2)
        
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
            time.sleep(5)

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
            
    # Return missed hrefs
    def return_missed_hrefs(self):
        return self.player_missed_hrefs

    # Scapa team stats
    def scrape_data(self, player_links, season_text):
        # Initialise Selenium webdriver
        driver = webdriver.Chrome() 

        # Try open url
        try:
            # Loop through player links
            for index, player_href in enumerate(player_links):
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
                    print('Completed: ', index, ' Total: ', len(player_links))
            
                except Exception as e:
                    # Print error
                    self.player_missed_hrefs.append(player_href)
                    print(f"An error occurred at {index} for {player_links[index]}:", str(e))
                
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

            return self.player_hrefs
                        
        except Exception as e:
            print("An error occurred:", str(e))
        
        finally:
            # Close the browser window
            driver.quit()