"""
Product Researcher Agent
Searches for products based on structured query information.
"""

from typing import List
from app.models.schemas import Product, StructuredQuery
from app.infrastructure.external_apis.serperdev_client import SerperDevClient


class ProductResearcherAgent:
    """Agent that searches for products based on structured query."""
    
    def __init__(self):
        """Initialize the product researcher with SerperDev."""
        self.serper_client = SerperDevClient()
    
    def search(self, structured_query: StructuredQuery, num_results: int = 10) -> List[Product]:
        """
        Search for products based on structured query.
        
        Args:
            structured_query: Structured query with product information
            num_results: Number of results to return
            
        Returns:
            List of Product objects
        """
        # Build optimized search query (include delivery_location in query if specified)
        search_query = self._build_search_query(structured_query)
        
        # Search with SerperDev (pass location if specified)
        try:
            # Use delivery_location if available, otherwise use location
            search_location = structured_query.delivery_location or structured_query.location
            products = self.serper_client.search_products(
                search_query, 
                num_results=num_results,
                location=structured_query.location  # Use country-level location for API
            )
        except Exception as e:
            raise Exception(f"SerperDev search failed: {str(e)}")
        
        # Filter by price if specified
        if structured_query.max_price or structured_query.min_price:
            products = self._filter_by_price(products, structured_query)
        
        return products[:num_results]
    
    def _build_search_query(self, structured_query: StructuredQuery) -> str:
        """
        Build an optimized search query from structured information.
        
        Args:
            structured_query: Structured query information
            
        Returns:
            Optimized search query string
        """
        # Use the query_text if available and good, otherwise build from components
        if structured_query.query_text and len(structured_query.query_text) > 10:
            query = structured_query.query_text
        else:
            # Build query from components
            parts = []
            
            if structured_query.brand:
                parts.append(structured_query.brand)
            
            if structured_query.product_type:
                parts.append(structured_query.product_type)
            
            if structured_query.category:
                parts.append(structured_query.category)
            
            # Add features
            for feature in structured_query.features[:3]:  # Limit to 3 features
                parts.append(feature)
            
            # Add price constraint to query text if not already included
            query = " ".join(parts) if parts else "product"
            
            if structured_query.max_price:
                # Add price in both dollars and euros for better search results
                max_usd = int(structured_query.max_price / 0.92)  # Convert back to USD for search
                query += f" under {max_usd} dollars"
            
            if structured_query.min_price:
                min_usd = int(structured_query.min_price / 0.92)  # Convert back to USD for search
                query += f" above {min_usd} dollars"
        
        # Add delivery location to query if specified (for better local results)
        if structured_query.delivery_location:
            query += f" {structured_query.delivery_location}"
        
        # Add condition to query if specified (e.g., "new", "used", "refurbished")
        if structured_query.condition:
            query += f" {structured_query.condition}"
        
        # Add style to query if specified (e.g., "casual", "formal", "sport")
        if structured_query.style:
            query += f" {structured_query.style}"
        
        # Note: Country-level location is handled via SerperDev API parameter (gl),
        # while city/neighborhood, condition, and style are added to query string for better targeting
        
        return query
    
    def _filter_by_price(self, products: List[Product], structured_query: StructuredQuery) -> List[Product]:
        """
        Filter products by price constraints.
        
        Args:
            products: List of products
            structured_query: Structured query with price constraints
            
        Returns:
            Filtered list of products
        """
        filtered = []
        
        for product in products:
            if not product.price:
                # If no price info, include it (let user decide)
                filtered.append(product)
                continue
            
            # Try to extract numeric price
            try:
                import re
                # Detect currency (dollar or euro)
                is_dollar = "$" in product.price or "dollar" in product.price.lower()
                
                # Remove currency symbols and extract number
                price_str = product.price.replace("€", "").replace("$", "").replace(",", "").strip()
                # Extract first number found
                numbers = re.findall(r'\d+\.?\d*', price_str)
                if numbers:
                    price_value = float(numbers[0])
                    
                    # Convert dollars to euros if needed (1 USD = 0.92 EUR)
                    if is_dollar:
                        price_value = price_value * 0.92
                    
                    # Check constraints (all prices now in euros)
                    if structured_query.max_price and price_value > structured_query.max_price:
                        continue
                    if structured_query.min_price and price_value < structured_query.min_price:
                        continue
                    
                    filtered.append(product)
                else:
                    # Can't parse price, include it anyway
                    filtered.append(product)
            except:
                # Can't parse price, include it anyway
                filtered.append(product)
        
        return filtered

