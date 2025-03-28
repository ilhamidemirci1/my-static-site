import feedparser
import datetime
import json
import os
from bs4 import BeautifulSoup
from email.utils import parsedate_tz, mktime_tz

# RSS feed URL
rss_url = 'https://azure.microsoft.com/en-us/blog/feed/'

# Parse the RSS feed
feed = feedparser.parse(rss_url)


links=[]

for entry in feed.entries:
    content = entry.get('content', [])
    if content: 
        html_content = content[0].get('value', '')
        soup = BeautifulSoup(html_content, 'html.parser')

       # Bağlantıları al
        for link in soup.find_all('a', href=True):
            link_info = {
                'id': entry.get('id', 'unknown_id'),  # Makale id'si
                'phrase': link.get_text(strip=True),
                'phrase_url': link['href']
            }
            links.append(link_info)

# Linkleri JSON dosyasına kaydet
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"rss_links_{timestamp}.json"
save_path = os.path.join(os.getcwd(), file_name)

with open(save_path, "w", encoding="utf-8") as json_file:
    json.dump(links, json_file, indent=2, ensure_ascii=False)

print(f"Links saved to {file_name}")
 