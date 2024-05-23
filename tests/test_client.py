import pytest
from unittest.mock import MagicMock
from pycolbertdb.client import Colbertdb, Collection


@pytest.fixture
def colbertdb():
    return Colbertdb(url="http://localhost:8000", api_key="API_KEY")


def test_connect(colbertdb):
    # Mock the _post method to return a response with an access token
    colbertdb._post = MagicMock(return_value={"access_token": "TOKEN"})
    colbertdb.connect()
    assert colbertdb.access_token == "TOKEN"


def test_create_collection(colbertdb):
    # Mock the _post method to return a response with the created collection
    colbertdb._post = MagicMock(return_value={"name": "my_collection"})

    collection = colbertdb.create_collection(
        "my_collection", [{"content": "doc1"}, {"content": "doc2"}]
    )

    assert isinstance(collection, Collection)
    assert collection.name == "my_collection"
    assert collection.client == colbertdb


def test_create_collection_error(colbertdb):
    # Mock the _post method to return a response with the created collection
    colbertdb._post = MagicMock(return_value={"name": "my_collection"})

    with pytest.raises(Exception) as e:
        colbertdb.create_collection("my_collection", [])
        assert str(e.value) == "Documents must not be empty"


def test_search_collection(colbertdb):
    # Mock the _post method to return a response with the search results
    colbertdb._post = MagicMock(return_value={"results": []})

    response = colbertdb.search_collection("my_collection", "query", 10)

    assert response == {"results": []}


def test_delete_documents(colbertdb):
    # Mock the _post method to return a response with the deletion status
    colbertdb._post = MagicMock(return_value={"status": "success"})

    response = colbertdb.delete_documents("my_collection", ["doc1", "doc2"])

    assert response == {"status": "success"}


def test_add_to_collection(colbertdb):
    # Mock the _post method to return a response with the addition status
    colbertdb._post = MagicMock(return_value={"status": "success"})

    response = colbertdb.add_to_collection("my_collection", [{"content": "doc1"}])

    assert response == {"status": "success"}


def test_delete_collection(colbertdb):
    # Mock the _delete method to return a response with the deletion status
    colbertdb._delete = MagicMock(return_value={"status": "success"})

    response = colbertdb.delete_collection("my_collection")

    assert response == {"status": "success"}
