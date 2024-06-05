from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field
import requests

from pycolbertdb.models import (
    CreateCollectionRequest,
    CreateCollectionsOptions,
    OperationResponse,
    SearchCollectionResponse,
    CreateCollectionDocument,
)

TIMEOUT = 60


class Collection:
    """
    Represents a collection in the Colbertdb database.

    Args:
        name (str): The name of the collection.
        client (Colbertdb): The client object used to interact with the Colbertdb server.

    Attributes:
        name (str): The name of the collection.
        client (Colbertdb): The client object used to interact with the Colbertdb server.
    """

    def __init__(self, name: str, client):
        self.name: str = name
        self.client: Colbertdb = client

    def search(self, query: str, k: Optional[int] = None) -> SearchCollectionResponse:
        """
        Searches the collection for documents matching the given query.

        Args:
            query (str): The query string.
            k (Optional[int]): The maximum number of documents to retrieve (default: None).

        Returns:
            dict: A dictionary containing the search results.
        """
        response = self.client.search_collection(self.name, query=query, k=k)
        return SearchCollectionResponse(documents=response["documents"])

    def delete_documents(self, document_ids: List[str]) -> "Collection":
        """
        Deletes the specified documents from the collection.

        Args:
            document_ids (List[str]): A list of document IDs to delete.

        Returns:
            dict: A dictionary containing the deletion status.
        """
        self.client.delete_documents(self.name, document_ids)
        return self

    def add_documents(self, documents: List[Dict[str, Any]]) -> "Collection":
        """
        Adds the specified documents to the collection.

        Args:
            documents (List[Dict[str, Any]]): A list of documents to add.

        Returns:
            dict: A dictionary containing the addition status.
        """
        self.client.add_to_collection(self.name, documents)
        return self

    def delete(self) -> Dict[str, Any]:
        """
        Deletes the entire collection.

        Returns:
            dict: A dictionary containing the deletion status.
        """
        return self.client.delete_collection(self.name)


class Colbertdb(BaseModel):
    """
    A client for interacting with the Colbertdb API.

    Args:
        url (str): The URL of the Colbertdb server.
        api_key (str, optional): The API key for authentication. Defaults to None.

    Attributes:
        url (str): The URL of the Colbertdb server.
        api_key (str): The API key for authentication.
        access_token (str): The access token for authentication.

    Methods:
        _post: Sends a POST request to the Colbertdb server.
        _delete: Sends a DELETE request to the Colbertdb server.
        connect: Connects to the Colbertdb server and retrieves an access token.
        create_collection: Creates a new collection in the Colbertdb server.
        search_collection: Performs a search query on a collection in the Colbertdb server.
        delete_documents: Deletes documents from a collection in the Colbertdb server.
        add_to_collection: Adds documents to a collection in the Colbertdb server.
        delete_collection: Deletes a collection from the Colbertdb server.
    """

    url: str = Field(..., title="The URL of the Colbertdb server")
    api_key: Optional[str] = Field(None, title="The API key for authentication")
    store_name: Optional[str] = Field("default", title="The name of the store")
    access_token: Optional[str] = Field(
        None, title="The access token for authentication"
    )

    def __init__(
        self,
        url: str,
        api_key: Optional[str] = None,
        store_name: Optional[str] = "default",
    ):
        super().__init__(url=url, api_key=api_key, store_name=store_name)
        self._connect()

    def _connect(self) -> Dict[str, Any]:
        """
        Connects to the Colbertdb server and retrieves an access token.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        response = requests.post(
            f"{self.url}/api/v1/client/connect/{self.store_name}",
            headers={"x-api-key": self.api_key},
            timeout=TIMEOUT,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Failed to connect to the Colbertdb server - {response.json()['detail']}"
            )
        self.access_token = response.json()["access_token"]

    def _get(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a GET request to the Colbertdb server.

        Args:
            path (str): The path of the API endpoint.
            data (Dict[str, Any]): The data to be sent in the request body.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        response = requests.get(
            f"{self.url}/api/v1/collections{path}",
            json=data,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a POST request to the Colbertdb server.

        Args:
            path (str): The path of the API endpoint.
            data (Dict[str, Any]): The data to be sent in the request body.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        # This method is a placeholder for the actual implementation.
        response = requests.post(
            f"{self.url}/api/v1/collections{path}",
            json=data,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def _delete(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a DELETE request to the Colbertdb server.

        Args:
            path (str): The path of the API endpoint.
            data (Dict[str, Any]): The data to be sent in the request body.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        response = requests.delete(
            f"{self.url}/api/v1/collections{path}",
            json=data,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def create_collection(
        self,
        name: str,
        documents: List[CreateCollectionDocument],
        options: Optional[CreateCollectionsOptions] = None,
    ) -> Collection:
        """
        Creates a new collection in the Colbertdb server.

        Args:
            name (str): The name of the collection.
            documents (List[Dict[str, Any]]): The documents to be added to the collection.
            options (Dict[str, Any], optional): Additional options for creating the collection. Defaults to None.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        if len(documents) == 0:
            raise ValueError("At least one document must be provided.")
        if options is None:
            options = CreateCollectionsOptions()
        data = CreateCollectionRequest(
            name=name, documents=documents, options=options
        ).model_dump()
        self._post("/", data)
        return Collection(name, self)

    def list_collections(self) -> List[str]:
        """
        Lists the collections in the Colbertdb server.

        Returns:
            List[str]: A list of collection names.
        """
        response = self._get("/", {})
        return response["collections"]

    def load_collection(self, name: str) -> Union[Collection, ValueError]:
        """
        Loads an existing collection from the Colbertdb server.

        Args:
            name (str): The name of the collection to load.

        Returns:
            Collection: The loaded collection object.
        """
        response = self._get(f"/{name}", {})
        if not response["exists"]:
            raise ValueError(f"Collection '{name}' does not exist.")
        return Collection(name, self)

    def search_collection(
        self, name: str, query: str, k: Optional[int] = None
    ) -> SearchCollectionResponse:
        """
        Performs a search query on a collection in the Colbertdb server.

        Args:
            query (str): The search query.
            k (int, optional): The number of results to retrieve. Defaults to None.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        data = {"query": query, "k": k}
        return self._post(f"/{name}/search", data)

    def delete_documents(self, name: str, document_ids: List[str]) -> OperationResponse:
        """
        Deletes documents from a collection in the Colbertdb server.

        Args:
            document_ids (List[str]): The IDs of the documents to be deleted.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        data = {"document_ids": document_ids}
        return self._post(f"/{name}/delete", data)

    def add_to_collection(
        self, name: str, documents: List[CreateCollectionDocument]
    ) -> OperationResponse:
        """
        Adds documents to a collection in the Colbertdb server.

        Args:
            documents (List[Dict[str, Any]]): The documents to be added to the collection.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        data = {"documents": documents}
        return self._post(f"/{name}/documents", data)

    def delete_collection(self, name: str) -> OperationResponse:
        """
        Deletes a collection from the Colbertdb server.

        Args:
            name (str): The name of the collection to be deleted.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        return self._delete(f"/{name}", {})
