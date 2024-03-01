import importlib
import os
import shutil
import subprocess
import pandas as pd

# Import the module
helper_module_name = "helper_class"
helper_module = importlib.import_module(helper_module_name)

Helper = helper_module.Helper()

season = '2023/24'

# Find archived file 'premier_league_data.csv' path
archive_path = os.path.join('../archived_data', 'premier_league_data.csv')
Helper.delete_file(archive_path)

# Find raw file 'premier_league_data.csv' path
source_path = os.path.join('../raw_data/csv', 'premier_league_data.csv')
Helper.copy_from_location1_to_location2(source_path, archive_path)

# Get the absolute path of the script
script_path = os.path.join(os.getcwd(), "Webscrape Classes", "webscrape_classes.py")

# Run the script using subprocess
subprocess.run(["python", script_path])

# Import the module
module_name = "Webscrape Classes.webscrape_classes"
module = importlib.import_module(module_name)

LeagueTableScraper = module.LeagueTableScraper()

# Set url
url = 'https://www.premierleague.com/tables'

# Scrape premier league data for all seasons
premier_league = LeagueTableScraper.scrape_data(season, url)

# Save data to df
premier_league_new_season = pd.DataFrame(premier_league['premier_league'])

# Read the CSV file into a DataFrame
premier_league_old = pd.read_csv('../raw_data/csv/premier_league_data.csv')

premier_league_without_season = premier_league_old[premier_league_old['season'] != season]

premier_league_new = pd.concat([premier_league_new_season, premier_league_without_season])

# Find archived file 'premier_league_data.csv' path
raw_path = os.path.join('../raw_data/csv', 'premier_league_data.csv')
Helper.delete_file(raw_path)

export_path = '../raw_data/csv/premier_league_data.csv'

# Export data to xlsx
try:
    premier_league_new.to_csv(export_path, index=False)
    print(f'Succesfully exported premier_league_new to {export_path}')
except Exception as e:
    # Print error
        print(f'Error saving premier_league_new to {export_path}', str(e))

