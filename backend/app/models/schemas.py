from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Product(BaseModel):
    """Product schema."""
    name: str
    description: Optional[str] = None
    price: Optional[str] = None
    link: str
    platform: Optional[str] = None
    image: Optional[str] = None


class SearchRequest(BaseModel):
    """Search request schema."""
    query: str = Field(..., description="Search query")


class SearchResponse(BaseModel):
    """Search response schema."""
    query: str
    products: List[Product]
    total: int


class ChatRequest(BaseModel):
    """Chat request schema."""
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for iterative searches")


class StructuredQuery(BaseModel):
    """Structured query extracted from user message."""
    product_type: str
    category: Optional[str] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    brand: Optional[str] = None
    features: List[str] = []
    query_text: str
    location: Optional[str] = Field(None, description="Country or region (e.g., 'canada', 'france', 'usa')")
    delivery_location: Optional[str] = Field(None, description="City, neighborhood, or specific delivery address (e.g., 'montreal', 'cote-des-neiges', 'toronto downtown')")
    condition: Optional[str] = Field(None, description="Product condition (e.g., 'new', 'used', 'refurbished', 'neuf', 'occasion')")
    style: Optional[str] = Field(None, description="Product style (e.g., 'casual', 'formal', 'sport', 'vintage', 'modern')")


class ChatResponse(BaseModel):
    """Chat response schema."""
    message: str
    structured_query: Optional[StructuredQuery] = None
    products: Optional[List[Product]] = None
    session_id: Optional[str] = Field(None, description="Session ID for iterative searches")
    price_comparison: Optional[Dict[str, Any]] = Field(None, description="Price comparison results")
    conversational_response: Optional[str] = Field(None, description="Text response for conversational queries")
    product_message: Optional[str] = Field(None, description="Contextual message accompanying product results")
    error: Optional[str] = Field(None, description="Error message if any")
