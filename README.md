# Quickstart Guide for `pycolbertdb`

This quickstart guide provides instructions on how to use the `pycolbertdb` package to integrate ColbertDB with LlamaIndex, leveraging OpenAI's GPT-4 model for processing and querying documents.

## Prerequisites

Ensure you have the following installed and configured:

- Python 3.x
- An OpenAI API key
- Environment variables configured for ColbertDB

## Installation

1. **Install the necessary packages**

   ```sh
   pip install pycolbertdb -U
   pip install llama-index
   pip install llama-index-readers-web
   pip install requests
   pip install python-dotenv
   ```

## Code Example

Below is an example of how to use the `pycolbertdb` package to fetch, process, and query documents.

### Import Dependencies

Start by importing the necessary dependencies.

```python
import os
from dotenv import load_dotenv
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import Document, PromptTemplate
from llama_index.llms.openai import OpenAI

from pycolbertdb.client import Colbertdb
from pycolbertdb.models import CreateCollectionDocument
from pycolbertdb.helpers import from_llama_index_documents
```

### Load Environment Variables

Load your environment variables from a `.env` file.

```python
load_dotenv()
URL = os.getenv('COLBERTDB_URL')
API_KEY = os.getenv('COLBERTDB_API_KEY')
STORE_NAME = os.getenv('COLBERTDB_STORE_NAME')
OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')

URLS = ['https://en.wikipedia.org/wiki/Onigiri']
```

### Initialize Clients

Initialize the ColbertDB and OpenAI clients.

```python
client = Colbertdb(url=URL, api_key=API_KEY, store_name=STORE_NAME)
open_ai_client = OpenAI(model="gpt-4-turbo", api_key=OPEN_AI_KEY)

qa_prompt_tmpl_str = """\
Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, answer the query.
Please write the answer in the style of {tone_name}
Query: {query_str}
Answer: \
"""

prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
```

### Fetch and Process Documents

Fetch and process HTML content from the specified URLs.

```python
docs = from_llama_index_documents(SimpleWebPageReader(html_to_text=True).load_data(URLS))
```

### Create a Collection in ColbertDB

Create a new collection in ColbertDB with the processed documents.

```python
collection = client.create_collection(documents=docs, name='rice_ball_facts', options={"force_create": True})
```

### Search the Collection

Perform a search query on the created collection.

```python
result = collection.search(query="What are some popular fillings for onigiri?", k=3)
```

### Generate a Response Using OpenAI

Format the retrieved documents and generate a response using OpenAI.

```python
context = ''
for document in result.documents:
    print("Source: " + document.metadata['source'] + "\n", document.content)
    context += (document.content + "\n\n")

prompt = prompt_tmpl.format(context_str=context, tone_name="shakespeare", query_str="What are some typical onigiri fillings")
response = open_ai_client.complete(prompt)
print(response)
```

### Add New Documents to the Collection

Fetch additional documents and add them to the existing collection.

```python
new_docs = SimpleWebPageReader(html_to_text=True).load_data(["https://en.wikipedia.org/wiki/Kewpie_(mayonnaise)"])
new_formatted = [{"content": doc.text, "metadata": {"source": doc.id_}} for doc in new_docs[0:2]]

collection = collection.add_documents(documents=new_formatted)
```

### Search the Updated Collection

Perform a new search query on the updated collection.

```python
new_result = collection.search(query="When was kewpie mayo founded?", k=3)
new_context = ''
for document in new_result.documents:
    print("Source: " + document.metadata['source'] + "\n", document.content)
    new_context += (document.content + "\n\n")

prompt = prompt_tmpl.format(context_str=new_context, tone_name="bruce springsteen", query_str="When and where was kewpie mayo founded")
new_response = open_ai_client.complete(prompt)
print(new_response)
```

## Conclusion

This guide provides a quickstart overview of using the `pycolbertdb` package for document processing and querying. Customize the prompt and collection as needed for your specific use case.