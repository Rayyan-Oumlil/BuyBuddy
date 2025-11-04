"""
State definition for LangGraph shopping workflow.
"""

from typing import TypedDict, List, Optional, Dict, Any
from app.models.schemas import StructuredQuery, Product


class ShoppingState(TypedDict):
    """State for the shopping workflow."""
    # Input
    user_message: str
    session_id: Optional[str]
    
    # Step 1: Understanding
    structured_query: Optional[StructuredQuery]
    
    # Step 2: Research
    products: List[Product]
    excluded_product_links: List[str]  # Links of products already shown
    
    # Step 3: Price Comparison
    price_comparison: Optional[Dict[str, Any]]  # Price comparison results
    
    # Step 4: Product Message
    product_message: Optional[str]  # Contextual message accompanying product results
    
    # Conversation handling
    is_conversational: bool
    conversational_response: Optional[str]  # Text response for conversational queries
    
    # Feedback detection
    is_negative_feedback: bool
    
    # Metadata
    error: Optional[str]

