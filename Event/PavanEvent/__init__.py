import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from urllib.parse import unquote
import datetime
import os

def main(event: func.EventGridEvent):
    logging.info("Event Grid Triggered for new Blob")

    # Event data
    blob_url = event.get_json().get("url")
    blob_name = unquote(blob_url.split("/")[-1])
    container_name = blob_url.split("/")[-2]
    
    BLOB_CONNECTION_STRING = (
        "DefaultEndpointsProtocol=https;"
        "AccountName=chiddireddypavan;"
        "AccountKey=VIhlAc/rtj6ePheCCI6OopkXkxMmjt+sAKVFZkxHUn39LR4Bqd7V1JJGnNJ+nQ1U3l5OebP/PmRG+AStkmW3wA==;"
        "EndpointSuffix=core.windows.net"
    )

    blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    COSMOS_URL = "https://chiddireddypavan.documents.azure.com:443/"
    COSMOS_KEY = (
        "AccountEndpoint=https://chiddireddypavan.documents.azure.com:443/;AccountKey=VdDOjBNguX8JPdZGhGHZspCbiba9pnMsKapuc0CKqE2xMogrUP3m2NG8y5O8eDaKanVe6Vm9RlDcACDbNN8y0A==;"
    )
    DATABASE_NAME = "DocumentsDB"
    CONTAINER_NAME = "Documents"

    cosmos_client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)
    database = cosmos_client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    blob_properties = blob_client.get_blob_properties()
    blob_bytes = blob_client.download_blob().readall()

    try:
        text_content = blob_bytes.decode("utf-8", errors="ignore")
    except:
        text_content = ""

    title = text_content.split("\n")[0].strip() if text_content else ""

    word_count = len(text_content.split()) if text_content else 0

    record = {
        "id": blob_name,
        "url": blob_url,
        "size": blob_properties.size,
        "title": title,
        "wordCount": word_count,
        "uploadedOn": datetime.datetime.utcnow().isoformat()
    }

    # Insert or update
    container.upsert_item(record)

    logging.info(f"✔ Indexed metadata for: {blob_name}")
