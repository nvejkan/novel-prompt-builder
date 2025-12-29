"""
Novel Writing Prompt Builder + Memory System
FastAPI Backend - Stateless Calculations Only
Storage is on Frontend (localStorage)
Port: 3010
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

from models import (
    SearchRequest,
    SearchResponse,
    MergePreviewRequest,
    MergePreviewResponse,
    MergeApplyRequest,
    MergeApplyResponse,
    BuildPromptRequest,
    BuildPromptResponse,
    ExtractPromptRequest,
    ExtractPromptResponse,
)
from services import search, merge, prompt

# Initialize FastAPI app
app = FastAPI(
    title="Novel Prompt Builder",
    description="A prompt builder with memory for novel writing. Backend is stateless - all data stored in browser.",
    version="1.0.0"
)

# Get directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ============================================================
# Page Routes
# ============================================================

@app.get("/")
async def page_prompt_builder():
    """Serve the main prompt builder page"""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/extract")
async def page_extract():
    """Serve the extraction prompt creator page"""
    return FileResponse(os.path.join(STATIC_DIR, "extract.html"))


@app.get("/memory")
async def page_memory():
    """Serve the memory management page"""
    return FileResponse(os.path.join(STATIC_DIR, "memory.html"))


# ============================================================
# Search API (Stateless)
# ============================================================

@app.post("/api/search", response_model=SearchResponse)
async def api_search(request: SearchRequest):
    """
    Find matching keys in text.
    Memory is passed from frontend, not stored on backend.
    """
    # Convert Pydantic models to dict
    memory_dict = {}
    for key, entry in request.memory.items():
        memory_dict[key] = {"type": entry.type, "desc": entry.desc}
    
    matched_keys = search.find_matches(request.text, memory_dict)
    
    return SearchResponse(matched_keys=matched_keys)


# ============================================================
# Merge API (Stateless)
# ============================================================

@app.post("/api/merge/preview", response_model=MergePreviewResponse)
async def api_merge_preview(request: MergePreviewRequest):
    """
    Preview merge operation.
    Both current and incoming data passed from frontend.
    """
    # Convert Pydantic models to dict
    current_dict = {}
    for key, entry in request.current.items():
        current_dict[key] = {"type": entry.type, "desc": entry.desc}
    
    incoming_dict = {}
    for key, entry in request.incoming.items():
        incoming_dict[key] = {"type": entry.type, "desc": entry.desc}
    
    # Validate incoming data
    is_valid, error = merge.validate_import_data(incoming_dict)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Analyze
    analysis = merge.analyze(current_dict, incoming_dict)
    
    return MergePreviewResponse(
        new=analysis["new"],
        update=analysis["update"],
        skip=analysis["skip"],
        summary=analysis["summary"]
    )


@app.post("/api/merge/apply", response_model=MergeApplyResponse)
async def api_merge_apply(request: MergeApplyRequest):
    """
    Apply merge and return new memory state.
    Frontend will save the returned merged data to localStorage.
    """
    # Convert Pydantic models to dict
    current_dict = {}
    for key, entry in request.current.items():
        current_dict[key] = {"type": entry.type, "desc": entry.desc}
    
    incoming_dict = {}
    for key, entry in request.incoming.items():
        incoming_dict[key] = {"type": entry.type, "desc": entry.desc}
    
    merged, stats = merge.apply_merge(
        current_dict,
        incoming_dict,
        request.selected_new_keys,
        request.selected_update_keys
    )
    
    # Convert back to response format
    merged_response = {}
    for key, value in merged.items():
        merged_response[key] = {"type": value["type"], "desc": value["desc"]}
    
    return MergeApplyResponse(
        merged=merged_response,
        added=stats["added"],
        updated=stats["updated"],
        skipped=stats["skipped"]
    )


# ============================================================
# Prompt API (Stateless)
# ============================================================

@app.post("/api/prompt/build", response_model=BuildPromptResponse)
async def api_build_prompt(request: BuildPromptRequest):
    """
    Build augmented prompt with memory context.
    Memory is passed from frontend.
    """
    # Convert Pydantic models to dict
    memory_dict = {}
    for key, entry in request.memory.items():
        memory_dict[key] = {"type": entry.type, "desc": entry.desc}
    
    built_prompt = prompt.build_augmented_prompt(
        request.story,
        request.matched_keys,
        memory_dict,
        request.instruction
    )
    
    return BuildPromptResponse(prompt=built_prompt)


@app.post("/api/prompt/extract", response_model=ExtractPromptResponse)
async def api_extract_prompt(request: ExtractPromptRequest):
    """Build extraction prompt for Gemini"""
    built_prompt = prompt.build_extraction_prompt(
        request.story,
        request.types
    )
    
    return ExtractPromptResponse(prompt=built_prompt)


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": "Novel Prompt Builder",
        "storage": "frontend (localStorage)",
        "backend": "stateless calculations only"
    }


# ============================================================
# Main Entry Point
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Novel Prompt Builder + Memory System")
    print("=" * 60)
    print(f"Server: http://localhost:3010")
    print(f"API Docs: http://localhost:3010/docs")
    print("")
    print("Storage: Frontend (localStorage)")
    print("Backend: Stateless calculations only")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3010,
        reload=True
    )