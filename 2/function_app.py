import azure.functions as func
import json
import logging
import os
import datetime
from openai import AzureOpenAI  # Import the Azure-specific client
from azure.cosmos import CosmosClient, exceptions

app = func.FunctionApp()

@app.function_name(name="ProcessArticles")
@app.schedule(schedule="0 0 */2 * * *", arg_name="mytimer", run_on_startup=False, use_monitor=True)
def ProcessArticles(mytimer: func.TimerRequest) -> None:
    logging.info('Processing articles from Cosmos DB with OpenAI.')

    try:
        # Load environment variables
        api_key = os.environ["OPENAI_API_KEY"]
        endpoint_full = os.environ["OPENAI_ENDPOINT"]
        cosmos_endpoint = os.environ["COSMOS_DB_ENDPOINT"]
        cosmos_key = os.environ["COSMOS_DB_KEY"]
        database_name = os.environ["COSMOS_DB_DATABASE"]
        container_name = os.environ["COSMOS_DB_CONTAINER"]

        # Extract the base endpoint for OpenAI
        endpoint = endpoint_full.split("/openai/deployments")[0]

        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-05-01-preview",
            azure_endpoint=endpoint
        )

        # Initialize Cosmos DB client
        cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
        database = cosmos_client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        # Query articles where processed is false
        query = "SELECT * FROM c WHERE c.processed = false"
        articles = list(container.query_items(query=query, enable_cross_partition_query=True))

        if not articles:
            logging.info("No unprocessed articles found.")
            return

        processed_articles = []

        # Process each article
        for article in articles:
            article_id = article.get('id', '')
            title = article.get('title', '')
            content = article.get('content', '')
            source = article.get('source', '')
            url = article.get('url', '')
            published_date = article.get('published_date', '')

            if not content:
                continue

            # Generate summary using Azure OpenAI
            summary_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes technical articles."},
                    {"role": "user", "content": f"Summarize this article in 3-4 sentences:\n\n{content}"}
                ],
                max_tokens=150,
                temperature=0.5
            )

            # Extract summary from response
            summary = summary_response.choices[0].message.content.strip()

            # Current date/time for processing timestamp
            process_date = datetime.datetime.now().isoformat()

            # Update the article with new fields
            article['processed'] = True
            article['ai_summary'] = summary
            article['process_date'] = process_date
            article['published'] = False
            article['publication_date'] = None

            # Upsert the updated article back into Cosmos DB
            container.upsert_item(article)

            # Add to processed articles list for response
            processed_articles.append({
                "id": article_id,
                "title": title,
                "source": source,
                "url": url,
                "ai_summary": summary,
                "process_date": process_date
            })

        logging.info(f"Processed articles: {json.dumps(processed_articles)}")

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Cosmos DB error: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")