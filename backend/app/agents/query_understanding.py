"""
Query Understanding Agent
Extracts structured information from user queries.
"""

from typing import Dict, Any, Optional
from app.infrastructure.llm import get_llm_provider
from app.core.config import settings


class QueryUnderstandingAgent:
    """Agent that understands user queries and extracts structured information."""
    
    def __init__(self, llm_provider=None):
        """Initialize the agent with an LLM provider."""
        self.llm = llm_provider or get_llm_provider()
        self.system_prompt = """You are a shopping assistant that understands user product queries.
Extract structured information from user messages and return it as JSON.

Key information to extract:
- product_type: The main product category in English (e.g., "laptop", "phone", "dress", "headphones")
- category: Subcategory or specific type in English (e.g., "gaming", "evening", "wireless")
- max_price: Maximum price in euros (convert dollars to euros: 1 USD = 0.92 EUR, round to nearest integer)
- min_price: Minimum price in euros (convert dollars to euros: 1 USD = 0.92 EUR, round to nearest integer)
- brand: Brand name (if mentioned)
- features: List of important features mentioned
- query_text: Optimized search query in ENGLISH for product search (translate to English, keep product terms)
- location: Country or region in lowercase (e.g., "canada", "france", "usa", "uk", "australia") - extract if user mentions a country/region
- delivery_location: City, neighborhood, or specific delivery address in lowercase (e.g., "montreal", "toronto", "cote-des-neiges", "paris", "new york") - extract if user mentions where they want delivery or where they are located
- condition: Product condition in English (e.g., "new", "used", "refurbished") - extract if user mentions "neuf", "occasion", "usagé", "reconditionné", "new", "used", "refurbished"
- style: Product style in English (e.g., "casual", "formal", "sport", "vintage", "modern", "classic") - extract if user mentions style preferences

IMPORTANT:
- Convert all prices to euros (1 USD ≈ 0.92 EUR)
- Translate product_type and query_text to English for better search results
- If user says "dollar" or "$", convert to euros
- Detect location/country mentions: "canada", "france", "usa", "canadian", "french", "in canada", "available in canada", etc.
- Detect delivery locations: cities ("montreal", "toronto", "paris"), neighborhoods ("cote-des-neiges", "downtown", "montreal"), delivery phrases ("deliver to", "ship to", "available in", "in montreal")
- Detect condition: "neuf" → "new", "occasion" → "used", "usagé" → "used", "reconditionné" → "refurbished"
- Detect style: "casual", "formel", "sport", "vintage", "moderne", etc. → translate to English

Return ONLY valid JSON with these fields. Use null for missing information."""

    def understand(self, user_message: str) -> Dict[str, Any]:
        """
        Understand a user query and extract structured information.
        
        Args:
            user_message: The user's message/query
            
        Returns:
            Dictionary with extracted information:
            {
                "product_type": str,
                "category": str | None,
                "max_price": float | None,
                "min_price": float | None,
                "brand": str | None,
                "features": List[str],
                "query_text": str
            }
        """
        prompt = f"""Analyze this user query and extract product information:

User query: "{user_message}"

Return JSON with:
- product_type: main product category in ENGLISH (e.g., "dress", "laptop", "phone")
- category: subcategory in ENGLISH (e.g., "evening", "gaming", "business")
- max_price: maximum price in EUROS (convert dollars: 1 USD = 0.92 EUR, round to integer)
- min_price: minimum price in EUROS (convert dollars: 1 USD = 0.92 EUR, round to integer)
- brand: brand name (null if not mentioned)
- features: list of features mentioned
- query_text: optimized search query in ENGLISH for product search (translate to English)
- location: country or region in lowercase (e.g., "canada", "france", "usa", "uk") - extract if mentioned
- delivery_location: city, neighborhood, or delivery address in lowercase (e.g., "montreal", "cote-des-neiges", "toronto downtown") - extract if user mentions where they want delivery
- condition: product condition in ENGLISH (e.g., "new", "used", "refurbished") - extract if mentioned
- style: product style in ENGLISH (e.g., "casual", "formal", "sport", "vintage") - extract if mentioned

Examples:
- "robe de soiree moins de 100 dollar" → product_type: "dress", category: "evening", max_price: 92, query_text: "evening dress under 100 dollars", location: null, delivery_location: null, condition: null, style: null
- "laptop gaming sous 1500€" → product_type: "laptop", category: "gaming", max_price: 1500, query_text: "gaming laptop under 1500 euros", location: null, delivery_location: null, condition: null, style: null
- "air force 1 that i can order in canada" → product_type: "shoes", category: "sneakers", query_text: "air force 1", location: "canada", delivery_location: null, condition: null, style: null
- "nike shoes available in france" → product_type: "shoes", brand: "nike", query_text: "nike shoes", location: "france", delivery_location: null, condition: null, style: null
- "air force 1 in montreal that can deliver to cote-des-neiges" → product_type: "shoes", query_text: "air force 1", location: "canada", delivery_location: "montreal cote-des-neiges", condition: null, style: null
- "shoes that can ship to toronto" → product_type: "shoes", query_text: "shoes", location: "canada", delivery_location: "toronto", condition: null, style: null
- "robe de soiree neuf formelle" → product_type: "dress", category: "evening", query_text: "formal evening dress", condition: "new", style: "formal"
- "sneakers occasion casual" → product_type: "shoes", category: "sneakers", query_text: "casual sneakers", condition: "used", style: "casual"
- "laptop gaming reconditionné" → product_type: "laptop", category: "gaming", query_text: "gaming laptop", condition: "refurbished", style: null
"""

        try:
            result = self.llm.generate_json(prompt, system_prompt=self.system_prompt)
            
            # Ensure all required fields exist with defaults
            structured_query = {
                "product_type": result.get("product_type", ""),
                "category": result.get("category"),
                "max_price": result.get("max_price"),
                "min_price": result.get("min_price"),
                "brand": result.get("brand"),
                "features": result.get("features", []),
                "query_text": result.get("query_text", user_message),
                "location": result.get("location"),
                "delivery_location": result.get("delivery_location"),
                "condition": result.get("condition"),
                "style": result.get("style")
            }
            
            return structured_query
            
        except Exception as e:
            # Fallback: return basic structure with original query
            return {
                "product_type": "",
                "category": None,
                "max_price": None,
                "min_price": None,
                "brand": None,
                "features": [],
                "query_text": user_message,
                "location": None,
                "delivery_location": None,
                "condition": None,
                "style": None
            }

