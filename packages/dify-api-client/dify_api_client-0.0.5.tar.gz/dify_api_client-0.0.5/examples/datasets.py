# Add chunks to a document

import os

import dotenv

from dify_client import DifyClient, models


dotenv.load_dotenv()

DIFY_API_BASE = os.getenv("DIFY_API_BASE")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")


client = DifyClient(api_key=DIFY_API_KEY, api_base=DIFY_API_BASE)

response = client.add_chunk_to_document(
    dataset_id="894f6555-f3a6-43a0-9891-579cd64beaa8",
    document_id="ef510e1a-41a7-4c15-99a2-34949412cba4",
    req=models.AddChunkToDocumentRequest(
        segments=[
            models.Segment(
                content="Hello, world!",
                answer="Hello, world!",
                keywords=["hello", "world"],
            )
        ]
    ),
)

print(response)
