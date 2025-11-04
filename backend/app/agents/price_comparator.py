"""
Price Comparator Agent
Compares prices across different platforms and identifies the best deal.
"""

from typing import List, Dict, Optional, Any
from app.models.schemas import Product
import re


class PriceComparatorAgent:
    """Agent that compares prices across products and platforms."""
    
    def __init__(self):
        """Initialize the price comparator agent."""
        pass
    
    def compare_prices(self, products: List[Product]) -> Dict[str, Any]:
        """
        Compare prices across products and identify the best deal.
        
        Args:
            products: List of products to compare
            
        Returns:
            Dictionary with comparison results:
            {
                "best_deal": Product with lowest price,
                "price_comparison": List of products sorted by price,
                "price_range": {"min": float, "max": float},
                "recommendation": str
            }
        """
        if not products:
            return {
                "best_deal": None,
                "price_comparison": [],
                "price_range": {"min": None, "max": None},
                "recommendation": "Aucun produit à comparer."
            }
        
        # Extract prices and sort products
        products_with_prices = []
        for product in products:
            price_value = self._extract_price(product.price)
            if price_value:
                products_with_prices.append({
                    "product": product,
                    "price": price_value
                })
        
        if not products_with_prices:
            return {
                "best_deal": None,
                "price_comparison": products,
                "price_range": {"min": None, "max": None},
                "recommendation": "Aucun prix disponible pour la comparaison."
            }
        
        # Sort by price (ascending)
        products_with_prices.sort(key=lambda x: x["price"])
        
        # Extract best deal
        best_deal = products_with_prices[0]["product"]
        min_price = products_with_prices[0]["price"]
        max_price = products_with_prices[-1]["price"]
        
        # Build sorted product list
        sorted_products = [item["product"] for item in products_with_prices]
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            best_deal, min_price, max_price, len(products_with_prices)
        )
        
        return {
            "best_deal": best_deal,
            "price_comparison": sorted_products,
            "price_range": {
                "min": min_price,
                "max": max_price
            },
            "recommendation": recommendation,
            "total_compared": len(products_with_prices)
        }
    
    def _extract_price(self, price_str: Optional[str]) -> Optional[float]:
        """
        Extract numeric price from price string.
        
        Args:
            price_str: Price string (e.g., "$1,299.99", "€1,299.99", "1299.99")
            
        Returns:
            Numeric price value or None if can't parse
        """
        if not price_str:
            return None
        
        try:
            # Remove currency symbols and common separators
            cleaned = price_str.replace("€", "").replace("$", "").replace("£", "")
            cleaned = cleaned.replace(",", "").strip()
            
            # Extract first number (handles formats like "$1,299.99" or "1299.99")
            numbers = re.findall(r'\d+\.?\d*', cleaned)
            if numbers:
                return float(numbers[0])
        except:
            pass
        
        return None
    
    def _generate_recommendation(
        self,
        best_deal: Product,
        min_price: float,
        max_price: float,
        total_compared: int
    ) -> str:
        """
        Generate a human-readable recommendation.
        
        Args:
            best_deal: Product with lowest price
            min_price: Minimum price found
            max_price: Maximum price found
            total_compared: Number of products compared
            
        Returns:
            Recommendation string
        """
        price_diff = max_price - min_price
        price_diff_percent = (price_diff / min_price * 100) if min_price > 0 else 0
        
        recommendation_parts = [
            f"🏆 Meilleur prix : {best_deal.price} sur {best_deal.platform or 'plateforme inconnue'}"
        ]
        
        if best_deal.name:
            recommendation_parts.append(f"Produit : {best_deal.name}")
        
        if total_compared > 1:
            recommendation_parts.append(
                f"Comparé {total_compared} produits avec prix allant de {min_price:.2f}€ à {max_price:.2f}€"
            )
            
            if price_diff_percent > 10:
                recommendation_parts.append(
                    f"Écart de prix : {price_diff:.2f}€ ({price_diff_percent:.1f}% de différence)"
                )
        
        return " | ".join(recommendation_parts)


