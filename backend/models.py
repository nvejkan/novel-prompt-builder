"""
Pydantic models for request/response validation
All operations are stateless - memory is passed from frontend
"""

from pydantic import BaseModel, Field
from typing import Optional


class MemoryEntry(BaseModel):
    """Single memory entry"""
    type: str
    desc: str


class SearchRequest(BaseModel):
    """Request to search for matching keys in text"""
    text: str = Field(..., description="Text to search in")
    memory: dict[str, MemoryEntry] = Field(..., description="Memory data from frontend")


class SearchResponse(BaseModel):
    """Response with matched keys"""
    matched_keys: list[str]


class MergePreviewRequest(BaseModel):
    """Request to preview merge - compare current with incoming"""
    current: dict[str, MemoryEntry] = Field(..., description="Current memory from frontend")
    incoming: dict[str, MemoryEntry] = Field(..., description="New data to merge")


class MergeItem(BaseModel):
    """Single item in merge preview"""
    key: str
    type: str
    desc: str
    old_type: Optional[str] = None
    old_desc: Optional[str] = None


class MergePreviewResponse(BaseModel):
    """Response with merge analysis"""
    new: list[MergeItem]
    update: list[MergeItem]
    skip: list[MergeItem]
    summary: dict[str, int]


class MergeApplyRequest(BaseModel):
    """Request to apply merge and get resulting memory"""
    current: dict[str, MemoryEntry] = Field(..., description="Current memory")
    incoming: dict[str, MemoryEntry] = Field(..., description="New data")
    selected_new_keys: list[str] = Field(..., description="New keys to add")
    selected_update_keys: list[str] = Field(..., description="Existing keys to update")


class MergeApplyResponse(BaseModel):
    """Response with merged memory and stats"""
    merged: dict[str, MemoryEntry]
    added: int
    updated: int
    skipped: int


class BuildPromptRequest(BaseModel):
    """Request to build augmented prompt"""
    story: str = Field(default="", description="User's story input")
    matched_keys: list[str] = Field(default=[], description="Keys to include")
    memory: dict[str, MemoryEntry] = Field(default={}, description="Memory data")
    instruction: Optional[str] = Field(None, description="Custom instruction")


class BuildPromptResponse(BaseModel):
    """Response with built prompt"""
    prompt: str


class ExtractPromptRequest(BaseModel):
    """Request to build extraction prompt"""
    story: str = Field(..., description="Story to extract from")
    types: list[str] = Field(..., description="Types to extract")


class ExtractPromptResponse(BaseModel):
    """Response with extraction prompt"""
    prompt: str