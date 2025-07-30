#!/usr/bin/env python3

from dify_client import DifyClient
from dify_client.models import CreateDocumentByTextRequest, ProcessRule


def test_create_document_by_text():
    """
    Test the create document by text API endpoint
    """
    # Initialize the client (replace with your API key and base URL)
    client = DifyClient(
        api_key="your_api_key_here",
        api_base="http://uat-dify-llm.torilab.ai/v1",
    )

    # Create the request
    request = CreateDocumentByTextRequest(
        name="test_document",
        text="This is a test document content for the knowledge base.",
        indexing_technique="high_quality",
        process_rule=ProcessRule(mode="automatic"),
    )

    # Make the API call
    try:
        dataset_id = "your_dataset_id_here"
        response = client.create_document_by_text(
            dataset_id=dataset_id, req=request
        )

        print("Document created successfully!")
        print(f"Document ID: {response.document.id}")
        print(f"Document Name: {response.document.name}")
        print(f"Indexing Status: {response.document.indexing_status}")
        print(f"Batch: {response.batch}")

    except Exception as e:
        print(f"Error creating document: {e}")


if __name__ == "__main__":
    test_create_document_by_text()
