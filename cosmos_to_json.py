import os
import json
from azure.cosmos import CosmosClient, exceptions

def load_local_settings():
    """Load environment variables from local.settings.json."""
    settings_file = "local.settings.json"
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            settings = json.load(file)
            for key, value in settings.get("Values", {}).items():
                os.environ[key] = value
    else:
        raise FileNotFoundError(f"{settings_file} not found in the current directory.")

def fetch_articles_from_cosmos():
    """Fetch articles from Cosmos DB and write to news1.json."""
    try:
        # Load environment variables
        load_local_settings()

        # Get Cosmos DB credentials
        endpoint = os.environ.get("COSMOS_DB_ENDPOINT")
        key = os.environ.get("COSMOS_DB_KEY")
        database_name = os.environ.get("COSMOS_DB_DATABASE")
        container_name = os.environ.get("COSMOS_DB_CONTAINER")

        if not all([endpoint, key, database_name, container_name]):
            raise ValueError("One or more Cosmos DB environment variables are missing.")

        # Initialize Cosmos DB client
        client = CosmosClient(endpoint, key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        # Query articles
        query = "SELECT * FROM c"
        articles = list(container.query_items(query=query, enable_cross_partition_query=True))

        if not articles:
            print("No articles found in Cosmos DB.")
            return False

        # Write articles to news1.json
        with open("news1.json", "w", encoding="utf-8") as file:
            json.dump({"articles": articles}, file, ensure_ascii=False, indent=4)

        print(f"✅ {len(articles)} article(s) written to news1.json.")
        return True

    except exceptions.CosmosHttpResponseError as e:
        print(f"❌ Cosmos DB error: {e}")
        return False
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return False