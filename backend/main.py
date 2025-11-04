"""FastAPI application for screenshot search."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from models import init_db, get_all_screenshots_metadata
from services.indexer import scan_and_index
from services.gpt5_service import chat_with_screenshots

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Screenshot Search API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    """Chat request model."""
    query: str


class ChatResponse(BaseModel):
    """Chat response model."""
    results: List[Dict[str, Any]]
    query: str


@app.on_event("startup")
async def startup_event():
    """Initialize database and index screenshots on startup."""
    print("🚀 Starting Screenshot Search API...")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables!")
        print("   Please create a .env file with your OpenAI API key")
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Index screenshots
    scan_and_index()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Screenshot Search API",
        "endpoints": {
            "chat": "POST /api/chat",
            "images": "GET /api/images/{filename}",
            "reindex": "POST /api/reindex"
        }
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint - search screenshots based on natural language query."""
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Get all screenshots with metadata
    screenshots = get_all_screenshots_metadata()
    
    if not screenshots:
        return ChatResponse(
            query=request.query,
            results=[]
        )
    
    # Search using GPT-5 agent
    try:
        results = search_screenshots(request.query, screenshots)
        return ChatResponse(
            query=request.query,
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.get("/api/images/{filename}")
async def get_image(filename: str):
    """Serve screenshot image files."""
    image_path = Path("../screenshots") / filename
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)


@app.post("/api/reindex")
async def reindex():
    """Manually trigger re-indexing of screenshots."""
    try:
        scan_and_index()
        screenshots = get_all_screenshots_metadata()
        return {
            "message": "Re-indexing complete",
            "total_screenshots": len(screenshots)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Re-indexing error: {str(e)}")


@app.get("/api/stats")
async def get_stats():
    """Get statistics about indexed screenshots."""
    screenshots = get_all_screenshots_metadata()
    return {
        "total_screenshots": len(screenshots),
        "screenshots": [
            {
                "filename": s["filename"],
                "indexed_at": s["indexed_at"]
            }
            for s in screenshots
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

