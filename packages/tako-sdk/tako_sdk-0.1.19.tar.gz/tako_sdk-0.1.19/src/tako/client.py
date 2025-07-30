import os
from typing import List, Optional
import requests
import httpx

from tako.types.common.exceptions import (
    RelevantResultsNotFoundException,
    raise_exception_from_response,
)
from tako.types.knowledge_search.types import (
    KnowledgeSearchOutputs,
    KnowledgeSearchResults,
    KnowledgeSearchSourceIndex,
)
from tako.types.visualize.types import TakoDataFormatDataset, VisualizeRequest

TAKO_API_KEY = os.getenv("TAKO_API_KEY", None)
TAKO_SERVER_URL = os.getenv("TAKO_SERVER_URL", "https://trytako.com/")
TAKO_API_VERSION = os.getenv("TAKO_API_VERSION", "v1")


class TakoClient:
    def __init__(
        self,
        api_key: Optional[str] = TAKO_API_KEY,
        server_url: Optional[str] = TAKO_SERVER_URL,
        api_version: Optional[str] = TAKO_API_VERSION,
    ):
        assert api_key is not None, "API key is required"
        self.api_key = api_key
        self.server_url = server_url
        self.api_version = api_version

    def knowledge_search(
        self,
        text: str,
        source_indexes: Optional[List[KnowledgeSearchSourceIndex]] = [
            KnowledgeSearchSourceIndex.TAKO,
        ],
    ) -> KnowledgeSearchResults:
        """
        Search for knowledge cards based on a text query.

        Args:
            text: The text to search for.
            source_indexes: The source indexes to search for.

        Returns:
            A list of knowledge search results.

        Raises:
            APIException: If the API returns an error.
        """
        url = f"{self.server_url}/api/{self.api_version}/knowledge_search"
        payload = {
            "inputs": {
                "text": text,
            },
        }
        if source_indexes:
            payload["source_indexes"] = source_indexes

        response = requests.post(url, json=payload, headers={"X-API-Key": self.api_key})
        try:
            # Based on the response, raise an exception if the response is an error
            raise_exception_from_response(response)
        except RelevantResultsNotFoundException:
            # For cases where no relevant results are found, return an empty list
            # instead of raising an exception
            return KnowledgeSearchResults(
                outputs=KnowledgeSearchOutputs(knowledge_cards=[])
            )

        return KnowledgeSearchResults.model_validate(response.json())

    def get_image(self, card_id: str) -> bytes:
        """
        Get an image for a knowledge card.

        Args:
            card_id: The ID of the knowledge card.

        Returns:
            The image as bytes.
        """
        url = f"{self.server_url}/api/{self.api_version}/image/{card_id}/"
        response = requests.get(
            url,
            headers={
                "Accept": "image/*",
            },
        )
        return response.content

    def beta_visualize(
        self,
        tako_formatted_dataset: Optional[TakoDataFormatDataset] = None,
        file_id: Optional[str] = None,
        query: Optional[str] = None,
    ) -> KnowledgeSearchResults:
        url = f"{self.server_url}/api/{self.api_version}/beta/visualize"
        if tako_formatted_dataset is None and file_id is None:
            raise ValueError(
                "Either tako_formatted_dataset or file_id must be provided"
            )
        if tako_formatted_dataset is not None and file_id is not None:
            raise ValueError(
                "Only one of tako_formatted_dataset or file_id must be provided"
            )
        visualize_request = VisualizeRequest(
            tako_formatted_dataset=tako_formatted_dataset,
            file_id=file_id,
            query=query,
        )
        payload = visualize_request.model_dump()
        response = requests.post(url, json=payload, headers={"X-API-Key": self.api_key})
        raise_exception_from_response(response)
        return KnowledgeSearchResults.model_validate(response.json())

    def beta_upload_file(self, file_path: str) -> str:
        url = f"{self.server_url}/api/{self.api_version}/beta/files"
        with open(file_path, "rb") as f:
            files = {"file_content": (os.path.basename(file_path), f)}
            data = {"file_name": os.path.basename(file_path)}
            response = requests.post(
                url,
                files=files,
                data=data,
                headers={"X-API-Key": self.api_key},
            )
        raise_exception_from_response(response)
        return response.json()["id"]


class AsyncTakoClient:
    def __init__(
        self,
        api_key: Optional[str] = TAKO_API_KEY,
        server_url: Optional[str] = TAKO_SERVER_URL,
        api_version: Optional[str] = TAKO_API_VERSION,
        default_timeout_seconds: Optional[float] = 30.0,
    ):
        assert api_key is not None, "API key is required"
        self.api_key = api_key
        self.server_url = server_url.strip("/")
        self.api_version = api_version
        self.default_timeout_seconds = default_timeout_seconds

    async def knowledge_search(
        self,
        text: str,
        source_indexes: Optional[List[KnowledgeSearchSourceIndex]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> KnowledgeSearchResults:
        """
        Async search for knowledge cards based on a text query.

        Args:
            text: The text to search for.
            source_indexes: The source indexes to search for.

        Returns:
            A list of knowledge search results.

        Raises:
            APIException: If the API returns an error.
        """
        # Trailing slash is required for httpx
        url = f"{self.server_url}/api/{self.api_version}/knowledge_search/"
        payload = {
            "inputs": {
                "text": text,
            },
        }
        if source_indexes:
            payload["source_indexes"] = source_indexes

        async with httpx.AsyncClient(
            timeout=timeout_seconds or self.default_timeout_seconds
        ) as client:
            response = await client.post(
                url, json=payload, headers={"X-API-Key": self.api_key}
            )
            return KnowledgeSearchResults.model_validate(response.json())

    async def get_image(
        self, card_id: str, timeout_seconds: Optional[float] = None
    ) -> bytes:
        """
        Async get an image for a knowledge card.

        Args:
            card_id: The ID of the knowledge card.

        Returns:
            The image as bytes.
        """
        # Trailing slash is required for httpx
        url = f"{self.server_url}/api/{self.api_version}/image/{card_id}/"
        async with httpx.AsyncClient(
            timeout=timeout_seconds or self.default_timeout_seconds
        ) as client:
            response = await client.get(
                url,
                headers={
                    "Accept": "image/*",
                },
            )
            return response.content

    async def beta_visualize(
        self,
        tako_formatted_dataset: Optional[TakoDataFormatDataset] = None,
        file_id: Optional[str] = None,
        query: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
    ) -> KnowledgeSearchResults:
        url = f"{self.server_url}/api/{self.api_version}/beta/visualize"
        if tako_formatted_dataset is None and file_id is None:
            raise ValueError(
                "Either tako_formatted_dataset or file_id must be provided"
            )
        if tako_formatted_dataset is not None and file_id is not None:
            raise ValueError(
                "Only one of tako_formatted_dataset or file_id must be provided"
            )
        visualize_request = VisualizeRequest(
            tako_formatted_dataset=tako_formatted_dataset,
            file_id=file_id,
            query=query,
        )
        payload = visualize_request.model_dump()
        async with httpx.AsyncClient(
            timeout=timeout_seconds or self.default_timeout_seconds
        ) as client:
            response = await client.post(
                url, json=payload, headers={"X-API-Key": self.api_key}
            )
            raise_exception_from_response(response)
            return KnowledgeSearchResults.model_validate(response.json())
        
    async def beta_upload_file(self, file_content: bytes, file_name: str, timeout_seconds: Optional[float] = None) -> str:
        url = f"{self.server_url}/api/{self.api_version}/beta/files"
        files = {
            "file_content": (file_name, file_content),
            "file_name": (None, file_name),  # (filename, value) for form fields, filename=None
        }
        async with httpx.AsyncClient(
            timeout=timeout_seconds or self.default_timeout_seconds
        ) as client:
            response = await client.post(
                url, files=files, headers={"X-API-Key": self.api_key}
            )
            raise_exception_from_response(response)
            return response.json()["id"]
