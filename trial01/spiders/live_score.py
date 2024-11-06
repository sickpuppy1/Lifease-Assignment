import requests
import re
import time
import concurrent.futures
from pprint import pprint

def process_data(data):
    """
    Function to process and structure the raw API data into a more readable format.
    
    Parameters:
    - data (dict): The raw JSON data from the API.
    
    Returns:
    - formatted_data (dict): Structured data for display.
    """
    # Structure data into sections
    formatted_data = {
        "Player Stats": [],
        "Over Summary": [],
        "Session Comparison": []
    }
    
    # Extract and format Player Stats
    if 'A' in data and 'B' in data:
        player_stats = {
            "Player": data.get('A', "Unknown"),
            "Runs": data.get('R', "0"),
            "Balls Faced": data.get('B', "0"),
            "Strike Rate": data.get('S', "-"),
            "Wickets Taken": data.get('ca', "0"),
            "Overs Bowled": data.get('cb', "0"),
        }
        formatted_data["Player Stats"].append(player_stats)
    
    # Extract and format Over Summary (sample data with format assumption)
    if 'd' in data:
        over_summary = {
            "Over": data.get('d', "0.0.0.0.0.0"),
            "Runs in Over": sum(map(int, data.get('d', "0.0.0.0.0.0").split('.'))),
            "Wickets in Over": data.get('f', "0")
        }
        formatted_data["Over Summary"].append(over_summary)
    
    # Extract and format Session Comparison
    if 'm' in data and 'n' in data:
        session_comparison = {
            "6 Over Score": data.get('m', "0"),
            "10 Over Score": data.get('n', "0"),
            "15 Over Score": data.get('o', "0"),
        }
        formatted_data["Session Comparison"].append(session_comparison)
    
    return formatted_data

def fetch_data_from_url(url):
    key_pattern = re.compile(r'/scoreboard/(.*?)/')
    match = key_pattern.search(url)
    
    if match:
        original_key = match.group(1)
        api_url = f"https://api-v1.com/v10/sV3.php?key={original_key}"
        
        while True:
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                
                data = response.json()
                structured_data = process_data(data)
                pprint(structured_data)
            
            except requests.RequestException as e:
                print(f"Error fetching data from {api_url}: {e}")
            
            time.sleep(1)

def fetch_continuous_data_from_live_urls(live_urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetch_data_from_url, live_urls)
