import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_indievox_events():
    events = []
    page = 0
    url = "https://www.indievox.com/activity/get-more-game-list"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.indievox.com/activity"
    }
    
    while True:
        params = {
            "type": "card",
            "offset": page,
            "startDate": "2024/12/02"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            if not response.text.strip():
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.select('.thumbnails.activity')
            
            if not cards:
                break
            
            for card in cards:
                link = card.find('a')
                event = {
                    'title': card.select_one('.multi_ellipsis').text.strip(),
                    'date': card.select_one('.date').text.strip(),
                    'image': card.select_one('img')['src'],
                    'link': 'https://www.indievox.com' + link['href'] if link else None,
                }
                events.append(event)
                
            page += 1
            
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    return pd.DataFrame(events)

if __name__ == "__main__":
    df = scrape_indievox_events()
    print(df)
    df.to_csv('indievox_events.csv', index=False)