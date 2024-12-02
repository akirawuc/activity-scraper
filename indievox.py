import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_game_details(event_id):
    url = f"https://www.indievox.com/activity/game/{event_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rows = soup.select('#gameList table tbody tr')
        if not rows:
            return []
            
        details = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 4:
                detail = {
                    'datetime': cells[0].text.strip(),
                    'venue': cells[2].text.strip(),
                    'status': cells[3].text.strip()
                }
                print(detail)
                details.append(detail)
        return details
        
    except requests.RequestException:
        return []

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
                if not link:
                    continue
                
                event_id = link['href'].split('/')[-1]
                game_details = get_game_details(event_id)
                
                base_event = {
                    'title': card.select_one('.multi_ellipsis').text.strip(),
                    'image': card.select_one('img')['src'],
                    'link': 'https://www.indievox.com' + link['href'],
                }
                
                if game_details:
                    for detail in game_details:
                        event = base_event.copy()
                        event.update(detail)
                        events.append(event)
                else:
                    events.append(base_event)
                
            page += 1
            
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    return pd.DataFrame(events)

if __name__ == "__main__":
    df = scrape_indievox_events()
    print(df)
    df.to_csv('indievox_events.csv', index=False)