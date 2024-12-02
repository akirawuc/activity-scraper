import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_indievox_events():
    url = "https://www.indievox.com/activity"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    events = []
    panels = soup.find_all('div', class_='panel-body')
    
    for panel in panels:
        cards = panel.select('.thumbnails.activity')
        for card in cards:
            link = card.find('a')
            event = {
                'title': card.select_one('.multi_ellipsis').text.strip(),
                'date': card.select_one('.date').text.strip(),
                'image': card.select_one('img')['src'],
                'link': 'https://www.indievox.com' + link['href'] if link else None,
            }
            events.append(event)
    
    return pd.DataFrame(events)

if __name__ == "__main__":
    df = scrape_indievox_events()
    print(df)
    df.to_csv('indievox_events.csv', index=False)