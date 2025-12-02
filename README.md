This project automatically indexes any newly uploaded blob into Cosmos DB.
Whenever a file is added to the documents container, Event Grid triggers an Azure Function that reads metadata and content and saves a record into Cosmos DB.

What I built
An Event Grid Trigger Function
A Cosmos DB container called Documents
Storage container called documents

How it works
I upload a file into the documents container.
Blob Storage emits a BlobCreated event.
Event Grid sends this event to my Function.

  The function extracts:
   blob name
   URL
   size
   content type
   title (first line or H1 for text files)
   word count (only for text files)

It stores everything in Cosmos DB with id = blobName.
The function ignores duplicates using upsert.

Logic improvements I added:
I checked file extension to decide if the file is text.
For text files, I downloaded the blob and counted the words.
For non-text files, I still stored in metadata.
Used upsert to avoid duplicate insert errors.


What I tested:
Verified Event Grid triggers properly on blob upload
Checked the downloaded metadata
Successfully inserted documents into Cosmos DB
