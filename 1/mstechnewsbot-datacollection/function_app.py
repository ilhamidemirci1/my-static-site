import feedparser
import datetime
import os
from bs4 import BeautifulSoup
from email.utils import parsedate_tz, mktime_tz
from azure.cosmos import CosmosClient
import re
import logging
import datetime

import azure.functions as func


COSMOS_ENDPOINT = "https://mstechnewsbotcosmosdb.documents.azure.com:443/"
COSMOS_KEY = "64YHEhKacdk2JEtLD8U7x2bdAVKdrA6XqxX3P0pAI5YMGMln79h1Wj3C7DkUJMhF3T11hsAIK5TOACDbRAPi3A=="
DATABASE_NAME = "RSSFeedDB"
CONTAINER_NAME = "Articles"


client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)


rss_urls = [
    'https://azure.microsoft.com/en-us/blog/feed/',  
    'https://devblogs.microsoft.com/feed'
]

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f'Python timer trigger function ran at {utc_timestamp}')

for rss_url in rss_urls:
    feed = feedparser.parse(rss_url)

    for entry in feed.entries:
    
        published_date = "unknown"
        if hasattr(entry, "published"):
            try:
                published_date_tuple = parsedate_tz(entry.published)
                if published_date_tuple:
                    published_date_obj = datetime.datetime.fromtimestamp(mktime_tz(published_date_tuple), datetime.UTC)
                    published_date = published_date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception as e:
                print(f"Error parsing published date: {e}")

       
        content = entry.content[0].value if "content" in entry else ""

        #HTML temizleme
        soup = BeautifulSoup(content, "html.parser")

        
        phrase_refs = {link.get_text(strip=True): link['href'] for link in soup.find_all('a', href=True)}

        
        clean_content = soup.get_text().replace("\n", " ").replace("\r", "").replace("\t", " ")


        safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', entry.id)
        
        document = {
            'id': safe_id,
            'title': entry.title,
            'source': entry.link,
            'content': clean_content,
            'url': entry.link,
            'published_date': published_date,
            'processed': False,
            'phrase_refs': phrase_refs
        }
        
        try:
            container.create_item(body=document)
            print(f"Inserted: {entry.title}")
        except Exception as e:
            print(f"Error inserting document: {e}")

print("RSS feed verileri Cosmos DB'ye kaydedildi.")
