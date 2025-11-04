"""
SQLite repository for conversations, products, and searches.
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlite3 import Row

from app.core.database import get_db
from app.models.schemas import Product, StructuredQuery


class SQLiteRepository:
    """
    Repository for SQLite operations.
    """
    
    def save_conversation(
        self,
        session_id: str,
        user_message: str,
        assistant_response: Optional[str] = None,
        structured_query: Optional[StructuredQuery] = None
    ) -> int:
        """
        Save a conversation to the database.
        
        Args:
            session_id: Session identifier
            user_message: User's message
            assistant_response: Assistant's response text
            structured_query: Structured query object
            
        Returns:
            ID of the saved conversation
        """
        with get_db() as conn:
            cursor = conn.cursor()
            structured_query_json = json.dumps(structured_query.model_dump()) if structured_query else None
            
            cursor.execute("""
                INSERT INTO conversations (session_id, user_message, assistant_response, structured_query)
                VALUES (?, ?, ?, ?)
            """, (session_id, user_message, assistant_response, structured_query_json))
            
            return cursor.lastrowid
    
    def get_conversation_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversation dictionaries
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM conversations
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (session_id, limit))
            
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def save_search(
        self,
        session_id: Optional[str],
        query_text: str,
        structured_query: Optional[StructuredQuery] = None,
        num_results: int = 0
    ) -> int:
        """
        Save a search to the database.
        
        Args:
            session_id: Session identifier
            query_text: Search query text
            structured_query: Structured query object
            num_results: Number of results found
            
        Returns:
            ID of the saved search
        """
        with get_db() as conn:
            cursor = conn.cursor()
            structured_query_json = json.dumps(structured_query.model_dump()) if structured_query else None
            
            cursor.execute("""
                INSERT INTO searches (session_id, query_text, structured_query, num_results)
                VALUES (?, ?, ?, ?)
            """, (session_id, query_text, structured_query_json, num_results))
            
            return cursor.lastrowid
    
    def get_search_history(
        self,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get search history.
        
        Args:
            session_id: Optional session identifier to filter
            limit: Maximum number of searches to return
            
        Returns:
            List of search dictionaries
        """
        with get_db() as conn:
            cursor = conn.cursor()
            
            if session_id:
                cursor.execute("""
                    SELECT * FROM searches
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (session_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM searches
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))
            
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def cache_products(
        self,
        products: List[Product],
        search_query: str
    ) -> int:
        """
        Cache products in the database.
        
        Args:
            products: List of products to cache
            search_query: The query that found these products
            
        Returns:
            Number of products cached
        """
        cached_count = 0
        with get_db() as conn:
            cursor = conn.cursor()
            
            for product in products:
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO products 
                        (name, description, price, link, platform, image, search_query)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        product.name,
                        product.description,
                        product.price,
                        product.link,
                        product.platform,
                        product.image,
                        search_query
                    ))
                    cached_count += 1
                except Exception as e:
                    # Skip if product already exists (unique constraint on link)
                    print(f"Warning: Could not cache product {product.link}: {e}")
                    continue
        
        return cached_count
    
    def get_cached_products(
        self,
        search_query: str,
        limit: int = 10
    ) -> List[Product]:
        """
        Get cached products for a search query.
        
        Args:
            search_query: Search query text
            limit: Maximum number of products to return
            
        Returns:
            List of Product objects
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM products
                WHERE search_query LIKE ?
                ORDER BY cached_at DESC
                LIMIT ?
            """, (f"%{search_query}%", limit))
            
            rows = cursor.fetchall()
            products = []
            for row in rows:
                try:
                    product = Product(
                        name=row["name"],
                        description=row["description"] or "",
                        price=row["price"],
                        link=row["link"],
                        platform=row["platform"],
                        image=row["image"]
                    )
                    products.append(product)
                except Exception as e:
                    print(f"Warning: Could not parse cached product: {e}")
                    continue
            
            return products
    
    def _row_to_dict(self, row: Row) -> Dict[str, Any]:
        """
        Convert a SQLite row to a dictionary.
        """
        return {key: row[key] for key in row.keys()}

