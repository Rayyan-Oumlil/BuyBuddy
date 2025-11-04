"""
Simple in-memory session manager for iterative searches.
Will be replaced by SQLite in Milestone 10.
"""

from typing import Dict, Optional, List
from app.models.schemas import StructuredQuery, Product
import uuid


class SessionManager:
    """Simple in-memory session manager."""
    
    def __init__(self):
        """Initialize the session manager."""
        self.sessions: Dict[str, SessionData] = {}
    
    def create_session(self) -> str:
        """
        Create a new session.
        
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = SessionData(
            session_id=session_id,
            excluded_product_links=[],
            last_structured_query=None
        )
        return session_id
    
    def get_session(self, session_id: str) -> Optional['SessionData']:
        """
        Get session data.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None if not found
        """
        return self.sessions.get(session_id)
    
    def update_session(
        self,
        session_id: str,
        excluded_links: List[str],
        structured_query: Optional[StructuredQuery] = None
    ):
        """
        Update session data.
        
        Args:
            session_id: Session ID
            excluded_links: List of excluded product links
            structured_query: Last structured query (optional)
        """
        if session_id in self.sessions:
            self.sessions[session_id].excluded_product_links = excluded_links
            if structured_query:
                self.sessions[session_id].last_structured_query = structured_query


class SessionData:
    """Session data structure."""
    
    def __init__(
        self,
        session_id: str,
        excluded_product_links: List[str],
        last_structured_query: Optional[StructuredQuery]
    ):
        """Initialize session data."""
        self.session_id = session_id
        self.excluded_product_links = excluded_product_links
        self.last_structured_query = last_structured_query


# Global session manager instance
session_manager = SessionManager()

