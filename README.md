# colbertDB Python Client
This is a Python client for [colbertDB](https://www.github.com/colbertdb/colbertdb). It provides a simple interface for managing collections and documents, and for performing searches within collections.

## Features
- Create and manage collections: Easily create new collections and manage existing ones.
- Add and delete documents: Add new documents to collections and delete existing ones.
- Search collections: Perform search queries on collections and retrieve relevant documents.

## Installation
```
pip install pycolbertdb
```

## Usage
```python
from colbertdb.client import Colbertdb
from llama_index.readers.web import SimpleWebPageReader

client = Colbertdb(url="http://localhost:8080")
client.connect()

docs = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://www.radar.com/documentation/api"]
)
docs = [{"content": doc.text, "metadata": {"source": doc.id_}} for doc in docs]
collection = colbertdb.create_collection(collection_name, documents=docs)
response = collection.search(query="How do I add a geofence?", k=3)
print(response)
```
