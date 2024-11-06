import requests
import time
import re

def fetch_continuous_data_from_live_urls(live_urls):
    """
    Function to continuously fetch data from all URLs in the live_urls array.
    
    Parameters:
    - live_urls (list): List of live URLs to extract keys and fetch data from.
    
    Returns:
    - None: Prints data received from each API call.
    """
    # Regular expression pattern to extract the key from the URL
    key_pattern = re.compile(r'/scoreboard/(.*?)/')
    
    # Loop over each URL in live_urls
    for url in live_urls:
        # Extract the key from the URL using regex
        match = key_pattern.search(url)
        
        if match:
            original_key = match.group(1)
            
            # Generate modified keys by replacing the last three characters in the key
            for i in range(1000):  # Loop for 1000 iterations as an example
                modified_key = original_key[:-3] + f'{i:03d}'  # Replace last three chars with new ones
                api_url = f"https://api-v1.com/v10/sV3.php?key={modified_key}"

                try:
                    # Make a request to the API
                    response = requests.get(api_url)
                    response.raise_for_status()
                    
                    # Process or print the API data
                    data = response.json()
                    print(f"Data for {api_url}: {data}")
                
                except requests.RequestException as e:
                    print(f"Error fetching data from {api_url}: {e}")
                
                # Optional: add a delay to avoid excessive API calls
                time.sleep(1)

# Example usage
live_urls = [
    'https://crex.live/scoreboard/RSF/1P1/12th-Match/HH/HL/jam-vs-wni-12th-match-super-50-cup-2024/scorecard',
    # Add more URLs as needed
]

fetch_continuous_data_from_live_urls(live_urls)
