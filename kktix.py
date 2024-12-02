import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_kktix_events():
    url = "https://kktix.com/events"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    events = []
    event_cards = soup.select('ul.events li')
    
    for card in event_cards:
        link = card.find('a')
        if not link:
            continue
            
        event = {
            'title': card.select_one('.event-title h2').text.strip(),
            'date': card.select_one('.date').text.strip(),
            'image': card.select_one('img')['src'],
            'link': link['href']
        }
        events.append(event)
    
    return pd.DataFrame(events)

if __name__ == "__main__":
    df = scrape_kktix_events()
    print(df)
    df.to_csv('kktix_events.csv', index=False)