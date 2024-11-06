import requests
from bs4 import BeautifulSoup
def scrape_data_from_urls(info_urls):
    """
    Function to scrape match data from a list of URLs.
    
    Parameters:
    - info_urls (list): A list of URLs to scrape data from.
    
    Returns:
    - list: A list of dictionaries with scraped match information.
    """
    scraped_data = []
    
    for url in info_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant match information
            match_info = {
                'url': url,
                'title': soup.find('h1').text if soup.find('h1') else 'No title',
                'date': soup.find('div', class_='match-date').text if soup.find('div', class_='match-date') else 'No date',
                'teams': [team.text for team in soup.find_all('span', class_='team-name')]  # Example team names
            }
            
            # Append the dictionary to the list
            scraped_data.append(match_info)

            # Optional: delay to avoid hitting the server too quickly
            # time.sleep(1)

        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
    
    return scraped_data