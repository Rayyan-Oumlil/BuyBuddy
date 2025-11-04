"""
LangGraph nodes for shopping workflow.
"""

from typing import Dict, Any
from app.workflows.state import ShoppingState
from app.agents.query_understanding import QueryUnderstandingAgent
from app.agents.product_researcher import ProductResearcherAgent
from app.agents.price_comparator import PriceComparatorAgent
from app.agents.conversation_handler import ConversationHandlerAgent
from app.models.schemas import StructuredQuery
from app.infrastructure.llm import get_llm_provider
import re


def understand_query_node(state: ShoppingState) -> Dict[str, Any]:
    """
    Node 1: Understand the user query and extract structured information.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with structured_query
    """
    try:
        understanding_agent = QueryUnderstandingAgent()
        structured_data = understanding_agent.understand(state["user_message"])
        
        # Ensure all required fields exist with defaults (including new fields)
        structured_data.setdefault("condition", None)
        structured_data.setdefault("style", None)
        
        structured_query = StructuredQuery(**structured_data)
        
        return {
            "structured_query": structured_query,
            "error": None
        }
    except Exception as e:
        # Log the error for debugging
        import traceback
        print(f"Error in understand_query_node: {str(e)}")
        print(traceback.format_exc())
        
        return {
            "structured_query": None,
            "error": f"Error understanding query: {str(e)}"
        }


def check_conversation_node(state: ShoppingState) -> Dict[str, Any]:
    """
    Node 0: Check if user message is a conversational query using LLM.
    Uses fast keyword detection first to avoid LLM call for obvious product searches.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with is_conversational flag and response
    """
    message = state.get("user_message", "").lower().strip()
    
    # Fast detection: if message contains obvious product keywords, skip LLM call
    # Include both French and English keywords to ensure language-independent detection
    product_keywords = [
        # Products
        "laptop", "phone", "smartphone", "dress", "robe", "shoes", "chaussures",
        "headphones", "écouteurs", "tablet", "tablette", "watch", "montre", "computer", "pc", "ordinateur",
        "gaming", "camera", "caméra", "tv", "television", "monitor", "écran",
        "keyboard", "mouse", "souris", "bag", "sac", "jacket", "veste",
        "shirt", "pants", "pantalon", "jeans", 
        # Price indicators
        "under", "moins de", "sous", "max", "maximum", "min", "minimum",
        # Buying/search intent
        "buy", "acheter", "price", "prix", "dollar", "euro", "€", "$",
        # Search verbs (CRITICAL: these indicate product search!)
        "trouver", "find", "cherche", "search", "recherche", "rechercher",
        "aide moi", "help me", "trouve", "trouve moi", "find me",
        # Product conditions
        "occasion", "used", "neuf", "new", "reconditionné", "refurbished", "usagé",
        # Brands/products
        "air force", "nike", "adidas", "samsung", "apple", "iphone"
    ]
    
    # If message contains product keywords, it's likely a product search - skip LLM
    if any(keyword in message for keyword in product_keywords):
        return {
            "is_conversational": False,
            "conversational_response": None
        }
    
    # For ambiguous cases (short messages, greetings, questions), use LLM
    try:
        conversation_handler = ConversationHandlerAgent()
        analysis = conversation_handler.analyze_message(message)
        
        return {
            "is_conversational": analysis.get("is_conversational", False),
            "conversational_response": analysis.get("response")
        }
    except Exception as e:
        # If LLM fails, assume it's a product search
        return {
            "is_conversational": False,
            "conversational_response": None
        }


def check_feedback_node(state: ShoppingState) -> Dict[str, Any]:
    """
    Node 1.5: Check if user message is negative feedback.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with is_negative_feedback flag
    """
    message = state.get("user_message", "").lower()
    
    # Patterns for negative feedback
    negative_patterns = [
        r"je n'aime pas",
        r"je n'aime pas ça",
        r"pas ça",
        r"pas intéressé",
        r"pas intéressée",
        r"je n'aime rien",
        r"aucun ne me plaît",
        r"aucune ne me plaît",
        r"pas convaincu",
        r"pas convaincue",
        r"show me more",
        r"montre moi autre chose",
        r"autre chose",
        r"différent",
        r"autre",
    ]
    
    is_negative = False
    for pattern in negative_patterns:
        if re.search(pattern, message):
            is_negative = True
            break
    
    return {
        "is_negative_feedback": is_negative
    }


def research_products_node(state: ShoppingState) -> Dict[str, Any]:
    """
    Node 2: Search for products based on structured query.
    Excludes products already shown if this is a negative feedback.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with products
    """
    # Check if we have a structured query
    if not state.get("structured_query"):
        return {
            "products": [],
            "error": "No structured query available"
        }
    
    try:
        researcher_agent = ProductResearcherAgent()
        excluded_links = state.get("excluded_product_links", [])
        
        # Search for more products if negative feedback (get more to exclude previous ones)
        num_results = 20 if state.get("is_negative_feedback") else 10
        
        products = researcher_agent.search(
            state["structured_query"],
            num_results=num_results
        )
        
        # Exclude products already shown
        if excluded_links:
            products = [p for p in products if p.link not in excluded_links]
        
        # Limit to 10 results
        products = products[:10]
        
        # Update excluded links with new products shown
        new_excluded_links = excluded_links + [p.link for p in products]
        
        return {
            "products": products,
            "excluded_product_links": new_excluded_links,
            "error": None
        }
    except Exception as e:
        return {
            "products": [],
            "error": f"Error researching products: {str(e)}"
        }


def compare_prices_node(state: ShoppingState) -> Dict[str, Any]:
    """
    Node 3: Compare prices across products and identify best deal.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with price comparison results
    """
    products = state.get("products", [])
    
    if not products:
        return {
            "price_comparison": None,
            "error": None
        }
    
    try:
        comparator_agent = PriceComparatorAgent()
        comparison_result = comparator_agent.compare_prices(products)
        
        return {
            "price_comparison": comparison_result,
            "error": None
        }
    except Exception as e:
        return {
            "price_comparison": None,
            "error": f"Error comparing prices: {str(e)}"
        }


def generate_product_message_node(state: ShoppingState) -> Dict[str, Any]:
    """
    Node 4: Generate a contextual message to accompany product results using LLM.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with product_message
    """
    products = state.get("products", [])
    structured_query = state.get("structured_query")
    price_comparison = state.get("price_comparison")
    user_message = state.get("user_message", "")
    
    # If no products, don't generate a message
    if not products:
        return {
            "product_message": None,
            "error": None
        }
    
    try:
        llm = get_llm_provider()
        
        # Build context about products
        num_products = len(products)
        product_type = structured_query.product_type if structured_query else "produits"
        category = structured_query.category if structured_query and structured_query.category else None
        location = structured_query.location if structured_query and structured_query.location else None
        delivery_location = structured_query.delivery_location if structured_query and structured_query.delivery_location else None
        
        # Get best price info if available
        best_price_info = ""
        if price_comparison:
            best_price = price_comparison.get("best_price")
            best_platform = price_comparison.get("best_platform")
            if best_price and best_platform:
                best_price_info = f"Le meilleur prix trouvé est {best_price} sur {best_platform}."
        
        # Build detailed product information for LLM
        product_details = []
        for i, product in enumerate(products[:5], 1):  # Top 5 products
            product_info = f"{i}. {product.name}"
            if product.price:
                product_info += f" - {product.price}"
            if product.platform:
                product_info += f" ({product.platform})"
            product_details.append(product_info)
        
        product_summary = "\n".join(product_details)
        
        # Extract unique platforms
        platforms = list(set([p.platform for p in products if p.platform]))
        platforms_text = ", ".join(platforms[:4])  # Top 4 platforms
        if len(platforms) > 4:
            platforms_text += f" et {len(platforms) - 4} autres"
        
        # Extract price range
        price_range = ""
        prices_with_values = []
        for p in products:
            if p.price:
                try:
                    import re
                    price_str = p.price.replace("€", "").replace("$", "").replace(",", "").strip()
                    numbers = re.findall(r'\d+\.?\d*', price_str)
                    if numbers:
                        prices_with_values.append(float(numbers[0]))
                except:
                    pass
        
        if prices_with_values:
            min_price = min(prices_with_values)
            max_price = max(prices_with_values)
            if min_price == max_price:
                price_range = f"Prix: {products[0].price}"
            else:
                # Find the actual price strings for min and max
                min_price_product = next((p for p in products if p.price and str(min_price) in p.price.replace(",", "")), None)
                max_price_product = next((p for p in products if p.price and str(max_price) in p.price.replace(",", "")), None)
                if min_price_product and max_price_product:
                    price_range = f"Prix de {min_price_product.price} à {max_price_product.price}"
        
        # Build location context
        location_context = ""
        if delivery_location:
            # Prefer delivery location (more specific)
            location_context = f" disponibles à {delivery_location.title()}"
        elif location:
            location_context = f" disponibles en {location.capitalize()}"
        
        # Build category context
        category_context = ""
        if category:
            category_context = f" {category}"
        
        # Determine language (French or English)
        is_french = any(word in user_message.lower() for word in ["je", "vous", "cherche", "moins", "sous", "euro", "€"])
        
        if is_french:
            system_prompt = """Tu es BuyBuddy, un assistant shopping amical et utile.
Génère un message naturel et amical en français pour présenter les résultats de recherche de produits.
Sois concis, amical et informatif. Mentionne le nombre de produits trouvés et la meilleure offre si disponible.
Garde-le court (1-2 phrases maximum).

IMPORTANT: Retourne UNIQUEMENT le texte du message, PAS de JSON, PAS d'explications, juste le message."""
            
            user_prompt = f"""Génère un message amical et informatif pour présenter ces résultats de recherche de produits à l'utilisateur.

Demande originale de l'utilisateur: "{user_message}"

Produits trouvés: {num_products} {product_type}{category_context}{location_context}

Détails des produits:
{product_summary}

{f"Plateformes disponibles: {platforms_text}" if platforms_text else ""}
{f"Gamme de prix: {price_range}" if price_range else ""}
{best_price_info}
{f"Lieu de livraison: {delivery_location.title()}" if delivery_location else ""}

Génère un message naturel et informatif qui:
- Reconnaît ce qu'ils cherchaient
- Mentionne le nombre de produits trouvés
- Mentionne brièvement 2-3 produits intéressants avec leurs prix
- Mentionne les plateformes principales si pertinentes
- Mentionne la meilleure offre si disponible
- Les encourage à vérifier les résultats

Sois amical, informatif mais concis (2-3 phrases maximum). Retourne UNIQUEMENT le texte du message, rien d'autre."""
        else:
            system_prompt = """You are BuyBuddy, a friendly shopping assistant. 
Generate a natural, helpful message in English to introduce product search results.
Be concise, friendly, and informative. Mention the number of products found and the best deal if available.
Keep it short (1-2 sentences max).

IMPORTANT: Return ONLY the message text, no JSON, no explanations, just the message."""
            
            user_prompt = f"""Generate a friendly and informative message to present these product search results to the user.

User's original request: "{user_message}"

Products found: {num_products} {product_type}{category_context}{location_context}

Product details:
{product_summary}

{f"Available platforms: {platforms_text}" if platforms_text else ""}
{f"Price range: {price_range}" if price_range else ""}
{best_price_info}
{f"Delivery location: {delivery_location.title()}" if delivery_location else ""}

Generate a natural and informative message that:
- Acknowledges what they were looking for
- Mentions the number of products found
- Briefly mentions 2-3 interesting products with their prices
- Mentions main platforms if relevant
- Mentions the best deal if available
- Encourages them to check the results

Be friendly, informative but concise (2-3 sentences max). Return ONLY the message text, nothing else."""

        try:
            # Generate message with LLM using generate() for direct text output
            message = None
            try:
                # Use generate() method which returns text directly
                message = llm.generate(user_prompt, system_prompt=system_prompt)
                
                # Clean up the message (remove any JSON formatting if present)
                if message:
                    message = message.strip()
                    # Remove JSON wrapper if present
                    if message.startswith("{") or message.startswith("["):
                        try:
                            import json
                            parsed = json.loads(message)
                            if isinstance(parsed, dict):
                                message = parsed.get("message") or parsed.get("response") or parsed.get("text") or message
                            elif isinstance(parsed, str):
                                message = parsed
                        except:
                            pass  # Keep original message if JSON parsing fails
                    
                    # Ensure message is not empty
                    if not message or len(message.strip()) == 0:
                        message = None
            except Exception as e:
                # If generate fails, use fallback
                message = None
            
            # Fallback if LLM doesn't return expected format
            if not message:
                # Generate simple fallback message
                if delivery_location:
                    message = f"J'ai trouvé {num_products} {product_type}{category_context} disponibles à {delivery_location.title()}."
                elif location:
                    message = f"J'ai trouvé {num_products} {product_type}{category_context} disponibles en {location.capitalize()}."
                else:
                    message = f"J'ai trouvé {num_products} {product_type}{category_context} pour vous."
                
                if best_price_info:
                    message += f" {best_price_info}"
            
            return {
                "product_message": message,
                "error": None
            }
        except Exception as e:
            # Fallback: generate simple message without LLM
            if delivery_location:
                fallback_message = f"J'ai trouvé {num_products} {product_type}{category_context} disponibles à {delivery_location.title()}."
            elif location:
                fallback_message = f"J'ai trouvé {num_products} {product_type}{category_context} disponibles en {location.capitalize()}."
            else:
                fallback_message = f"J'ai trouvé {num_products} {product_type}{category_context} pour vous."
            
            if best_price_info:
                fallback_message += f" {best_price_info}"
            
            return {
                "product_message": fallback_message,
                "error": None
            }
            
    except Exception as e:
        # Even if everything fails, provide a simple message
        num_products = len(state.get("products", []))
        if num_products > 0:
            return {
                "product_message": f"J'ai trouvé {num_products} produit{'s' if num_products > 1 else ''} correspondant à votre recherche.",
                "error": None
            }
        else:
            return {
                "product_message": None,
                "error": None
            }

