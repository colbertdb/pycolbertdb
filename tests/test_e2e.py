# import pytest

# from llama_index.readers.web import SimpleWebPageReader
# from pycolbertdb.client import Colbertdb


# @pytest.fixture
# def colbertdb():
#     client = Colbertdb(
#         url="http://localhost:8080", api_key="supersecret", store_name="default"
#     )
#     yield client


# def test_connect(colbertdb):
#     assert colbertdb.access_token is not None


# def test_end_to_end(colbertdb):
#     collection_name = "test_collection"
#     docs = SimpleWebPageReader(html_to_text=True).load_data(
#         ["https://www.radar.com/documentation"]
#     )
#     docs = [{"content": doc.text, "metadata": {"source": doc.id_}} for doc in docs]
#     collection = colbertdb.create_collection(collection_name, documents=docs)

#     assert collection.name == collection_name
#     assert collection.client == colbertdb

#     collections = colbertdb.list_collections()
#     assert collection_name in collections

#     docs_to_add = SimpleWebPageReader(html_to_text=True).load_data(
#         ["https://www.radar.com/documentation/api"]
#     )

#     docs_to_add = [
#         {"content": doc.text, "metadata": {"source": doc.id_}} for doc in docs_to_add
#     ]

#     collection.add_documents(documents=docs)
#     response = collection.search(query="How do I add a geofence?", k=3)
#     assert len(response.documents) == 3
#     doc_to_delete = response.documents[0].document_id
#     collection.delete_documents(document_ids=[doc_to_delete])
#     collection.delete()


# def test_load_collection(colbertdb):
#     collection_name = "test_collection_to_load"
#     docs = SimpleWebPageReader(html_to_text=True).load_data(
#         ["https://www.radar.com/documentation"]
#     )
#     docs = [{"content": doc.text, "metadata": {"source": doc.id_}} for doc in docs]
#     colbertdb.create_collection(collection_name, documents=docs)
#     collection = colbertdb.load_collection(name=collection_name)
#     response = collection.search(query="How do I add a geofence?", k=3)
#     assert len(response.documents) == 3
#     assert collection.name == collection_name
