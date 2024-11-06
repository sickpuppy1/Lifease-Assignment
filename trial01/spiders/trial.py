import requests
from bs4 import BeautifulSoup
import playersdata as pd  # Assuming this module has functions to fetch and parse player data
import live_score as ls   # Assuming this module has a function to fetch continuous live data
import matchinfo as mi
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Base URL for constructing full URLs
BASE_URL = 'https://crex.live'
MATCH_LIST_URL = 'https://crex.live/fixtures/match-list'

# URLs for specific data types
live_urls = []
scorecard_urls = []
info_urls = []
all_info_urls = []

def gather_info_urls(url):
    """
    Gather all relevant URLs from the match list page.
    
    Parameters:
    - url (str): The URL of the match list page.
    
    Returns:
    - None: Updates global lists for info, live, and scorecard URLs.
    """
    try:
        reqs = requests.get(url, timeout=10)
        reqs.raise_for_status()
        soup = BeautifulSoup(reqs.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = BASE_URL + href
            if '/scoreboard/' in href:
                if href.endswith('/live'):
                    live_urls.append(full_url)
                    all_info_urls.append(full_url.replace('/live', '/info'))
                elif href.endswith('/scorecard'):
                    scorecard_urls.append(full_url)
                    all_info_urls.append(full_url.replace('/scorecard', '/info'))
                else:
                    info_urls.append(full_url)
                    all_info_urls.append(full_url)
                    
        logging.info("URLs gathered successfully.")
    except requests.RequestException as e:
        logging.error(f"Error gathering URLs: {e}")

# Fetch all info URLs
gather_info_urls(MATCH_LIST_URL)

def scrape_and_display_match_info():
    """
    Scrape and display match information.
    
    Returns:
    - None: Prints scraped match information.
    """
    scraped_data = mi.scrape_data_from_urls(info_urls)
    print("Scraped Match Information:")
    print(scraped_data)
    print('\n')

def fetch_and_display_player_data():
    """
    Fetch and display combined player data from info URLs.
    
    Returns:
    - None: Prints combined player data.
    """
    all_players_data = []
    for url in info_urls:
        try:
            soup = pd.fetch_and_parse(url)  # Assumes pd.fetch_and_parse(url) returns parsed HTML
            players_data = pd.extract_player_data(soup)  # Assumes pd.extract_player_data extracts player data
            all_players_data.extend(players_data)
        except Exception as e:
            logging.error(f"Error fetching player data from {url}: {e}")
    
    print("Combined Player Data:")
    print(all_players_data)

def start_live_data_fetching():
    """
    Fetch continuous live data from gathered live URLs.
    
    Returns:
    - None: Initiates continuous live data fetching.
    """
    try:
        print("Fetching Continuous Live Data:")
        ls.fetch_continuous_data_from_live_urls(live_urls)
    except Exception as e:
        logging.error(f"Error fetching live data: {e}")

# Execution flow based on user input
def main():
    a = input("Enter your choice (1 for Match Info, 2 for Player Data, 3 for Live Data): ")
    
    if a == '1':
        scrape_and_display_match_info()
    elif a == '2':
        fetch_and_display_player_data()
    elif a == '3':
        start_live_data_fetching()
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
