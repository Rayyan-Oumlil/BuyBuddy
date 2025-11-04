"""
History endpoint to retrieve conversation and search history.
"""

from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
from app.infrastructure.repositories.sqlite_repository import SQLiteRepository

router = APIRouter()
repository = SQLiteRepository()


@router.get("/history/conversations")
async def get_conversation_history(
    session_id: Optional[str] = Query(None, description="Session ID to filter conversations"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of conversations to return")
) -> List[Dict[str, Any]]:
    """
    Get conversation history.
    
    Args:
        session_id: Optional session ID to filter conversations
        limit: Maximum number of conversations to return
        
    Returns:
        List of conversation dictionaries
    """
    if session_id:
        return repository.get_conversation_history(session_id, limit)
    else:
        # Return all conversations (limited)
        return repository.get_conversation_history("anonymous", limit)


@router.get("/history/searches")
async def get_search_history(
    session_id: Optional[str] = Query(None, description="Session ID to filter searches"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of searches to return")
) -> List[Dict[str, Any]]:
    """
    Get search history.
    
    Args:
        session_id: Optional session ID to filter searches
        limit: Maximum number of searches to return
        
    Returns:
        List of search dictionaries
    """
    return repository.get_search_history(session_id, limit)

