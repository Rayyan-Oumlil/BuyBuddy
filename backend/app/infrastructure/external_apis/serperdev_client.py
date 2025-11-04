import requests
from typing import List, Dict, Optional
from app.core.config import settings
from app.models.schemas import Product


class SerperDevClient:
    """Client for SerperDev API to search products."""
    
    # Mapping of country names to ISO country codes for SerperDev API
    COUNTRY_CODES = {
        "canada": "ca",
        "france": "fr",
        "usa": "us",
        "united states": "us",
        "uk": "gb",
        "united kingdom": "gb",
        "australia": "au",
        "germany": "de",
        "spain": "es",
        "italy": "it",
        "japan": "jp",
        "china": "cn",
        "india": "in",
        "brazil": "br",
        "mexico": "mx",
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.serper_api_key
        self.base_url = "https://google.serper.dev/search"
        self.shopping_url = "https://google.serper.dev/shopping"
    
    def _get_country_code(self, location: Optional[str] = None) -> str:
        """
        Convert location name to ISO country code for SerperDev API.
        
        Args:
            location: Country name in lowercase (e.g., "canada", "france")
            
        Returns:
            ISO country code (e.g., "ca", "fr") or "us" as default
        """
        if not location:
            return "us"  # Default to US
        
        location_lower = location.lower().strip()
        
        # Direct match
        if location_lower in self.COUNTRY_CODES:
            return self.COUNTRY_CODES[location_lower]
        
        # Check if location contains a country name
        for country, code in self.COUNTRY_CODES.items():
            if country in location_lower or location_lower in country:
                return code
        
        # If no match, default to US
        return "us"
    
    def search_products(self, query: str, num_results: int = 10, location: Optional[str] = None) -> List[Product]:
        """
        Search products using SerperDev API.
        
        Args:
            query: Search query (e.g., "laptop gaming under 1500 dollars")
            num_results: Number of results to return (default: 10)
            location: Country or region (e.g., "canada", "france") - will set gl parameter
            
        Returns:
            List of Product objects
        """
        if not self.api_key or self.api_key == "":
            raise ValueError("SerperDev API key is required. Set SERPER_API_KEY in .env")
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Get country code for geographic targeting
        country_code = self._get_country_code(location)
        
        products = []
        
        # Try Shopping endpoint first (better for products with prices)
        try:
            shopping_payload = {
                "q": query,
                "num": num_results,
                "gl": country_code,  # Geographic location (country code)
                "hl": "en"
            }
            
            shopping_response = requests.post(
                self.shopping_url, 
                json=shopping_payload, 
                headers=headers,
                timeout=10
            )
            shopping_response.raise_for_status()
            shopping_data = shopping_response.json()
            
            # Parse shopping results (these have prices!)
            # SerperDev shopping endpoint returns results in "shopping" array
            if "shopping" in shopping_data:
                for item in shopping_data["shopping"]:
                    # Use "source" field for platform if available, otherwise extract from link
                    platform = item.get("source", "")
                    if not platform:
                        platform = self._extract_platform(item.get("link", ""))
                    
                    product = Product(
                        name=item.get("title", ""),
                        price=item.get("price", ""),  # Price is directly in "price" field
                        description=item.get("snippet", ""),
                        link=item.get("link", ""),
                        platform=platform,
                        image=item.get("imageUrl", "") if "imageUrl" in item else None
                    )
                    products.append(product)
        except Exception as e:
            # If shopping endpoint fails, fall back to regular search
            pass
        
        # If we don't have enough results, try regular search
        if len(products) < num_results:
            try:
                search_payload = {
                    "q": f"{query} shopping buy",
                    "num": num_results - len(products),
                    "gl": country_code,  # Use same country code
                    "hl": "en"
                }
                
                search_response = requests.post(
                    self.base_url, 
                    json=search_payload, 
                    headers=headers,
                    timeout=10
                )
                search_response.raise_for_status()
                search_data = search_response.json()
                
                # Parse shopping results from regular search
                if "shopping" in search_data:
                    for item in search_data["shopping"]:
                        # Check if we already have this product (by link or title)
                        if not any(p.link == item.get("link") or p.name == item.get("title") for p in products):
                            platform = item.get("source", "")
                            if not platform:
                                platform = self._extract_platform(item.get("link", ""))
                            
                            product = Product(
                                name=item.get("title", ""),
                                price=item.get("price", ""),
                                description=item.get("snippet", ""),
                                link=item.get("link", ""),
                                platform=platform,
                                image=item.get("imageUrl", "") if "imageUrl" in item else None
                            )
                            products.append(product)
                
                # Parse organic results if we still need more
                if len(products) < num_results and "organic" in search_data:
                    for item in search_data["organic"]:
                        # Check if we already have this product
                        if not any(p.link == item.get("link") for p in products):
                            product = Product(
                                name=item.get("title", ""),
                                description=item.get("snippet", ""),
                                link=item.get("link", ""),
                                platform=self._extract_platform(item.get("link", "")),
                                image=item.get("imageUrl") if "imageUrl" in item else None
                            )
                            products.append(product)
                            if len(products) >= num_results:
                                break
            except Exception as e:
                raise Exception(f"Error searching products: {str(e)}")
        
        return products[:num_results]  # Limit to requested number
    
    def _extract_platform(self, url: str) -> str:
        """Extract platform name from URL."""
        if not url:
            return "Unknown"
        
        url_lower = url.lower()
        
        if "amazon" in url_lower:
            return "Amazon"
        elif "ebay" in url_lower:
            return "eBay"
        elif "walmart" in url_lower:
            return "Walmart"
        elif "bestbuy" in url_lower:
            return "Best Buy"
        elif "target" in url_lower:
            return "Target"
        elif "newegg" in url_lower:
            return "Newegg"
        else:
            # Extract domain name
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                # Remove www. and get main domain
                domain = domain.replace("www.", "").split(".")[0]
                return domain.capitalize()
            except:
                return "Unknown"

