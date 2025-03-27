
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

def main():
    try:
        # Load environment variables from local.settings.json
        load_local_settings()

        # Initialize Cosmos DB Client
        cosmos_endpoint = os.environ["COSMOS_DB_ENDPOINT"]
        cosmos_key = os.environ["COSMOS_DB_KEY"]
        database_name = os.environ["COSMOS_DB_DATABASE"]
        container_name = os.environ["COSMOS_DB_CONTAINER"]

        cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
        database = cosmos_client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        # Query articles where processed is false
        query = "SELECT * FROM c WHERE c.processed = false"
        articles = list(container.query_items(query=query, enable_cross_partition_query=True))

        # Print the retrieved articles
        if articles:
            print(f"Retrieved {len(articles)} unprocessed articles:")
            for article in articles:
                print(f"ID: {article['id']}, Title: {article['title']}, Processed: {article.get('processed', 'N/A')}")
        else:
            print("No unprocessed articles found.")

    except exceptions.CosmosHttpResponseError as e:
        print(f"Cosmos DB error: {e}")
    except KeyError as e:
        print(f"Missing environment variable: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()