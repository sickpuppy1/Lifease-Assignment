import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_and_parse(url):
    """
    Fetch the HTML content from the given URL and parse it using BeautifulSoup.
    
    Parameters:
    - url (str): The URL of the page to scrape.
    
    Returns:
    - BeautifulSoup object: Parsed HTML content.
    """
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_player_info(card):
    """
    Extract player data from a single player card.
    
    Parameters:
    - card (BeautifulSoup): The BeautifulSoup element representing a player card.
    
    Returns:
    - dict: A dictionary containing player details.
    """
    player_info = {}

    # Extract player name and role
    player_info['name'] = card.find('div', class_='p-name').get_text(strip=True) if card.find('div', class_='p-name') else 'No name'
    player_info['role'] = card.find('div', class_='bat-ball-type').get_text(strip=True) if card.find('div', class_='bat-ball-type') else 'No role'

    # Extract captain (C) or wicketkeeper (WK) designation if available
    designation_container = card.find('div', class_='flex')
    if designation_container:
        designation_tags = designation_container.find_all('div')
        player_info['designation'] = designation_tags[1].get_text(strip=True) if len(designation_tags) > 1 else "No designation"

   

    # Structure the data in a similar way to the image
    structured_data = {
        "Player Name": player_info['name'],
        "Role": player_info['role'],

    }

    return structured_data

def extract_player_data(soup):
    """
    Extract player data from the parsed HTML content, focusing only on essential details.
    
    Parameters:
    - soup (BeautifulSoup): Parsed HTML content containing player data.
    
    Returns:
    - list: A list of dictionaries, each containing key player details.
    """
    players_data = []
    
    # Find the section that contains player cards
    player_cards = soup.find_all('div', class_='playingxi-card-row')

    # Use ThreadPoolExecutor for parallel extraction
    with ThreadPoolExecutor() as executor:
        # Submit all the player card processing tasks
        future_to_card = {executor.submit(extract_player_info, card): card for card in player_cards}
        
        # Collect the results as they are completed
        for future in as_completed(future_to_card):
            player_info = future.result()
            players_data.append(player_info)
    
    return players_data

