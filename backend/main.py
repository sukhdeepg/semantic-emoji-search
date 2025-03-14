
import emoji
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any
from pydantic import BaseModel
import pathlib

# Import our modules
from emoji_data import emoji_dataset
from models import EmojiSearchModel

# Initialize the FastAPI app
app = FastAPI(
    title="Semantic Emoji Search",
    description="Search for emojis using deep learning semantic understanding",
    version="1.0.0",
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, will replace it with specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the model with our emoji dataset
emoji_search_model = EmojiSearchModel(emoji_dataset.get_all_emojis())

# Response model for emoji search
class EmojiSearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]

# Create a "frontend" directory path relative to this file for serving static files
FRONTEND_DIR = pathlib.Path(__file__).parent.parent / "frontend"

# API Routes
@app.get("/", tags=["Frontend"])
async def root():
    """
    Serve the frontend index.html file.
    """
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "API is running"}

@app.get("/api/emoji/groups", tags=["Emoji"])
async def get_emoji_groups() -> List[str]:
    """
    Get all emoji groups.
    
    Returns:
        List[str]: A list of all emoji groups.
    """
    return emoji_dataset.get_emoji_groups()

@app.get("/api/emoji/all", tags=["Emoji"])
async def get_all_emojis() -> List[Dict[str, Any]]:
    """
    Get all emojis.
    
    Returns:
        List[Dict[str, Any]]: A list of all emoji dictionaries.
    """
    return emoji_dataset.format_for_frontend()

@app.get("/api/emoji/group/{group}", tags=["Emoji"])
async def get_emojis_by_group(group: str) -> List[Dict[str, Any]]:
    """
    Get emojis filtered by group.
    
    Args:
        group (str): The emoji group to filter by.
        
    Returns:
        List[Dict[str, Any]]: A list of emoji dictionaries filtered by group.
    """
    emojis = emoji_dataset.get_emoji_by_group(group)
    if not emojis:
        raise HTTPException(status_code=404, detail=f"Group '{group}' not found")
    
    # Format emojis for frontend
    return [
        {
            "emoji": emoji.emojize(item["emoji"]),
            "name": item["name"],
            "group": item["group"]
        }
        for item in emojis
    ]

@app.get("/api/emoji/search", response_model=EmojiSearchResponse, tags=["Search"])
async def search_emojis(
    query: str = Query(..., description="Search query for emojis"),
    top_k: int = Query(20, description="Number of top results to return"),
) -> Dict[str, Any]:
    """
    Search for emojis based on the query.
    
    Args:
        query (str): The search query.
        top_k (int): Number of top results to return.
        
    Returns:
        Dict[str, Any]: The search results containing the query and matching emojis.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    # Search for emojis
    results = emoji_search_model.search(query, top_k=top_k)
    
    # Format results for frontend
    formatted_results = []
    for result in results:
        formatted_results.append({
            "emoji": emoji.emojize(result["emoji"]),
            "name": result["name"],
            "group": result["group"],
            "score": result["score"]
        })
    
    return {
        "query": query,
        "results": formatted_results
    }

# Mount the frontend files after the API routes
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 