import importlib
import os
import shutil
import subprocess
import pandas as pd

season = '2023/24'

# Import the module
helper_module_name = "helper_class"
helper_module = importlib.import_module(helper_module_name)

Helper = helper_module.Helper()

# Delete archived file
archive_path = os.path.join('../archived_data', 'player_stats_data.csv')
Helper.delete_file(archive_path)

# Copy raw file to archive
source_path = os.path.join('../raw_data/csv', 'player_stats_data.csv')
Helper.copy_from_location1_to_location2(source_path, archive_path)

# Get the absolute path of the script
script_path = os.path.join(os.getcwd(), "Webscrape Classes", "player_stats_class.py")

# Run the script using subprocess
subprocess.run(["python", script_path])

# Import the module
module_name = "Webscrape Classes.player_stats_class"
module = importlib.import_module(module_name)

PlayerStatsScraper = module.PlayerStatsScraper()

# Set url
url = 'https://www.premierleague.com/players'

try:
    # Get links
    player_links = PlayerStatsScraper.get_links(url)
    print(f"Successfully got {len(player_links)} player links")
except Exception as e:
    # Print error
        print(f'Error getting player links', str(e))

try:
    # Scrape player stats data
    player_stats = PlayerStatsScraper.scrape_data(player_links, season, False)
    print("Successfully got player stats")
except Exception as e:
    # Print error
        print(f'Error getting player stats', str(e))

try:
    # Scrape player stats data
    missed_links = PlayerStatsScraper.return_missed_hrefs()

    if len(missed_links) > 0:
        print(f"There were {len(missed_links)} missed links")
        player_stats = PlayerStatsScraper.scrape_data(missed_links, season, True)
        print(f"Successfully got {len(missed_links)} missed stats")
except Exception as e:
    # Print error
        print(f'Error getting missed player stats', str(e))

# Save data to df
player_stats_data = pd.DataFrame(player_stats['player_stats'])

# # Delete raw file
raw_path = os.path.join('../raw_data/csv', 'player_stats_data.csv')
Helper.delete_file(raw_path)

export_path = '../raw_data/csv/player_stats_data.csv'

# Export data to xlsx
try:
    player_stats_data.to_csv(export_path, index=False)
    print(f'Succesfully exported player_stats_data to {export_path}')
except Exception as e:
    # Print error
        print(f'Error saving player_stats_data to {export_path}', str(e))