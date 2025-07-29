"""
Hypermindz RAG Search Tool for CrewAI
=====================================

This module provides a semantic similarity search tool designed for Retrieval-Augmented
Generation (RAG) systems within CrewAI workflows.
"""

import os
from typing import Optional

import requests
from crewai.tools import tool


class HypermindzRAGSearchTool:
    """
    A class to encapsulate the Hypermindz RAG Search functionality.

    This tool performs semantic similarity searches over vectorized dataset collections
    to retrieve contextually relevant entries based on user queries.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        dataset_id: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize the RAG Search Tool.

        Args:
            base_url (Optional[str]): The base API URL. If None, reads from HYPERMINDZ_BASE_URL env var.
            dataset_id (Optional[str]): The dataset ID. If None, reads from HYPERMINDZ_DATASET_ID env var.
            api_key (Optional[str]): The API key. If None, reads from HYPERMINDZ_RAG_API_KEY env var.
        """
        self.base_url = base_url or os.getenv("HYPERMINDZ_BASE_URL")
        self.dataset_id = dataset_id or os.getenv("HYPERMINDZ_DATASET_ID")
        self.api_key = api_key or os.getenv("HYPERMINDZ_RAG_API_KEY")

        # Construct the API URL (without dataset ID in path)
        if self.base_url:
            # Remove trailing slash from base_url if present
            self.base_url = self.base_url.rstrip("/")
        self.api_url = f"{self.base_url}/search"

    def validate_config(self) -> tuple[bool, str]:
        """
        Validate the configuration.

        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not self.base_url:
            return (
                False,
                "Error: HYPERMINDZ_BASE_URL not provided or environment variable not set",
            )
        if not self.dataset_id:
            return (
                False,
                "Error: HYPERMINDZ_DATASET_ID not provided or environment variable not set",
            )
        if not self.api_key:
            return (
                False,
                "Error: HYPERMINDZ_RAG_API_KEY not provided or environment variable not set",
            )
        return True, ""

    def search(self, query_text: str, timeout: int = 30) -> str:
        """
        Perform a semantic similarity search.

        Args:
            query_text (str): The search query in natural language.
            timeout (int): Request timeout in seconds. Default is 30.

        Returns:
            str: Search results or error message.
        """
        # Validate configuration
        is_valid, error_msg = self.validate_config()
        if not is_valid:
            return error_msg

        try:
            params = {"query": query_text, "id": self.dataset_id}
            headers = {"Authorization": f"Bearer {self.api_key}"}

            response = requests.get(
                self.api_url, params=params, headers=headers, timeout=timeout
            )
            response.raise_for_status()

            # Parse and return results
            results = response.json().get("results", [])
            if not results:
                return "No relevant datasets found."

            return str(results)

        except requests.exceptions.RequestException as e:
            return f"API request error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


# CrewAI tool decorator version
@tool("Hypermindz RAG Search Tool")  # type: ignore[misc]
def hypermindz_rag_search(query_text: str) -> str:
    """
    Performs a semantic similarity search over a vectorized dataset collection to retrieve the most
    contextually relevant entries based on the user's input query.

    This tool is designed for use in Retrieval-Augmented Generation (RAG) systems and depends heavily
    on well-structured, natural language queries to return high-quality results. It sends the input query
    to a local or remote API that performs vector similarity matching within a predefined dataset collection.

    Args:
        query_text (str): A clear and descriptive query expressed in natural language.
            For best results, use full-sentence queries that capture specific intent
            (e.g., "List of climate-related policy documents published in 2023").

    Returns:
        str: A formatted string of the most relevant datasets found, or a message indicating
        no matches were found.

    Notes:
        - Optimized for semantic search in production RAG workflows.
        - Uses HYPERMINDZ_BASE_URL for the API endpoint and sends HYPERMINDZ_DATASET_ID as 'id' parameter.
        - Results depend on the clarity and specificity of the query provided.

    Environment Variables Required:
        - HYPERMINDZ_BASE_URL: The base URL of the Hypermindz API (e.g., https://api.hypermindz.com)
        - HYPERMINDZ_DATASET_ID: The specific dataset ID to search within (sent as 'id' parameter)
        - HYPERMINDZ_RAG_API_KEY: The API key for authentication

    Example:
        # Set environment variables:
        # HYPERMINDZ_BASE_URL=https://api.hypermindz.com
        # HYPERMINDZ_DATASET_ID=climate_data_2023
        # HYPERMINDZ_RAG_API_KEY=your_api_key_here

        # The tool will make a request to: https://api.hypermindz.com/search?query=your_query&id=climate_data_2023

        query_text = "Datasets about global energy consumption trends from the past decade"
        result = hypermindz_rag_search(query_text)
    """
    tool_instance = HypermindzRAGSearchTool()
    return tool_instance.search(query_text)


# Export both the class and the decorated function
__all__ = ["HypermindzRAGSearchTool", "hypermindz_rag_search"]
