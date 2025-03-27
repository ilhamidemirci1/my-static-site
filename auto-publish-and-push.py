import subprocess
from update_json import *
from cosmos_to_json import fetch_articles_from_cosmos

if fetch_articles_from_cosmos():
    subprocess.run(["python", "update_json.py"])

    # Git'e ekle, commit et ve push et
    subprocess.run(["git", "add", "news1.json"])
    subprocess.run(["git", "commit", "-m", "📰 Auto update from Cosmos DB"])
    subprocess.run(["git", "push"])
