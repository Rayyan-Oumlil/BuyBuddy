"""
History endpoint to retrieve conversation and search history.
"""

from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
from app.infrastructure.repositories.sqlite_repository import SQLiteRepository
from app.core.database import get_db
from app.models.schemas import Product

router = APIRouter()
repository = SQLiteRepository()


@router.get("/history/conversations")
async def get_conversation_history(
    session_id: Optional[str] = Query(None, description="Session ID to filter conversations"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of conversations to return")
) -> List[Dict[str, Any]]:
    """
    Get conversation history.
    If session_id is provided, returns conversations for that session.
    If not, returns all conversations grouped by session.
    
    Args:
        session_id: Optional session ID to filter conversations
        limit: Maximum number of conversations to return
        
    Returns:
        List of conversation dictionaries
    """
    if session_id:
        return repository.get_conversation_history(session_id, limit)
    else:
        # Get all conversations (we'll group them in frontend)
        # Get more to have enough for grouping
        all_conversations = []
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM conversations
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit * 2,))  # Get more to have enough after grouping
            rows = cursor.fetchall()
            all_conversations = [{key: row[key] for key in row.keys()} for row in rows]
        return all_conversations


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


@router.get("/history/conversation/{session_id}/products")
async def get_conversation_products(
    session_id: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum number of products to return")
) -> List[Dict[str, Any]]:
    """
    Get products for a specific conversation session.
    
    Args:
        session_id: Session ID to get products for
        limit: Maximum number of products to return
        
    Returns:
        List of product dictionaries with search_query
    """
    with get_db() as conn:
        cursor = conn.cursor()
        # Get searches for this session to get query_texts
        cursor.execute("""
            SELECT DISTINCT query_text 
            FROM searches 
            WHERE session_id = ?
        """, (session_id,))
        search_rows = cursor.fetchall()
        query_texts = [row["query_text"] for row in search_rows if row["query_text"]]
        
        # Get products that match any of the search queries
        products = []
        if query_texts:
            # Build query with multiple LIKE conditions
            placeholders = ','.join(['?' for _ in query_texts])
            cursor.execute(f"""
                SELECT DISTINCT p.* 
                FROM products p
                WHERE p.search_query IS NOT NULL
                AND (
                    {' OR '.join(['p.search_query LIKE ?' for _ in query_texts])}
                )
                ORDER BY p.cached_at DESC
                LIMIT ?
            """, [f'%{q}%' for q in query_texts] + [limit])
            
            rows = cursor.fetchall()
            for row in rows:
                try:
                    product_dict = {
                        "name": row["name"],
                        "description": row["description"] or "",
                        "price": row["price"],
                        "link": row["link"],
                        "platform": row["platform"],
                        "image": row["image"],
                        "search_query": row["search_query"]  # Include search_query for matching
                    }
                    products.append(product_dict)
                except Exception as e:
                    print(f"Warning: Could not parse product: {e}")
                    continue
        
        return products
