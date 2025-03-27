import os
import json
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions

# Cosmos DB bağlantısını kur
COSMOS_DB_ENDPOINT = os.environ["COSMOS_DB_ENDPOINT"]
COSMOS_DB_KEY = os.environ["COSMOS_DB_KEY"]
COSMOS_DB_DATABASE = os.environ["COSMOS_DB_DATABASE"]
COSMOS_DB_CONTAINER = os.environ["COSMOS_DB_CONTAINER"]

cosmos_client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
database = cosmos_client.get_database_client(COSMOS_DB_DATABASE)
container = database.get_container_client(COSMOS_DB_CONTAINER)

try:
    # published alanı false olan makaleleri sorgula
    query = "SELECT * FROM c WHERE c.published = false"
    articles = list(container.query_items(query=query, enable_cross_partition_query=True))

    if not articles:
        print("Güncellenecek makale bulunamadı.")
    else:
        # news1.json dosyasına yaz
        with open("news1.json", "w", encoding="utf-8") as file:
            json.dump({"articles": articles}, file, ensure_ascii=False, indent=4)

        print(f"✅ {len(articles)} makale news1.json dosyasına yazıldı.")

except exceptions.CosmosHttpResponseError as e:
    print(f"Cosmos DB hatası: {e}")
except Exception as e:
    print(f"Bir hata oluştu: {e}")
