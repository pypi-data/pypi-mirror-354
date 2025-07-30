from typing import List, Optional

from pydantic import BaseModel


class Segment(BaseModel):
    content: str
    answer: Optional[str] = None
    keywords: Optional[List[str]] = None


class AddChunkToDocumentRequest(BaseModel):
    segments: List[Segment]


class AddChunkToDocumentResponseDataItem(BaseModel):
    id: str
    position: int
    document_id: str
    content: str
    answer: Optional[str] = None
    word_count: int
    tokens: int
    keywords: List[str]
    index_node_id: str
    index_node_hash: str
    hit_count: int
    enabled: bool
    disabled_at: Optional[int] = None
    disabled_by: Optional[str] = None
    status: str
    created_by: str
    created_at: int
    indexing_at: int
    completed_at: int
    error: Optional[str] = None
    stopped_at: Optional[int] = None


class AddChunkToDocumentResponse(BaseModel):
    """

    {
    "data": [{
        "id": "",
        "position": 1,
        "document_id": "",
        "content": "1",
        "answer": "1",
        "word_count": 25,
        "tokens": 0,
        "keywords": [
        "a"
        ],
        "index_node_id": "",
        "index_node_hash": "",
        "hit_count": 0,
        "enabled": true,
        "disabled_at": null,
        "disabled_by": null,
        "status": "completed",
        "created_by": "",
        "created_at": 1695312007,
        "indexing_at": 1695312007,
        "completed_at": 1695312007,
        "error": null,
        "stopped_at": null
    }],
    "doc_form": "text_model"
    }
    """

    data: List[AddChunkToDocumentResponseDataItem]
    doc_form: str
