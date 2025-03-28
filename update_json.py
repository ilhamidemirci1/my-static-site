import os
import json
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions
from cosmos_to_json import load_local_settings

# Ayarları yükle
load_local_settings()

# Cosmos bağlantısı
COSMOS_DB_ENDPOINT = os.environ["COSMOS_DB_ENDPOINT"]
COSMOS_DB_KEY = os.environ["COSMOS_DB_KEY"]
COSMOS_DB_DATABASE = os.environ["COSMOS_DB_DATABASE"]
COSMOS_DB_CONTAINER = os.environ["COSMOS_DB_CONTAINER"]

cosmos_client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
database = cosmos_client.get_database_client(COSMOS_DB_DATABASE)
container = database.get_container_client(COSMOS_DB_CONTAINER)

now_iso = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

try:
    # Makaleleri getir
    query = "SELECT * FROM c"
    articles = list(container.query_items(query=query, enable_cross_partition_query=True))

    if not articles:
        print("Cosmos DB'den alınacak makale bulunamadı.")
    else:
        for article in articles:
            if not article.get("published"):
                article["published"] = True
                if "publication_date" not in article or article["publication_date"] in [None, ""]:
                    article["publication_date"] = now_iso

        # Güncellenmiş verileri dosyaya yaz
        with open("news1.json", "w", encoding="utf-8") as file:
            json.dump({"articles": articles}, file, ensure_ascii=False, indent=4)

        print(f"✅ {len(articles)} makale güncellendi ve news1.json dosyasına yazıldı.")

except exceptions.CosmosHttpResponseError as e:
    print(f"Cosmos DB hatası: {e}")
except Exception as e:
    print(f"Bir hata oluştu: {e}")
