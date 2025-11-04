"""
LangGraph shopping workflow.
Orchestrates the query understanding and product research agents.
"""

from langgraph.graph import StateGraph, END
from typing import Optional
from app.workflows.state import ShoppingState
from app.workflows.nodes import (
    understand_query_node,
    research_products_node,
    check_feedback_node,
    compare_prices_node,
    generate_product_message_node,
    check_conversation_node
)
from app.workflows.session_manager import session_manager
from app.models.schemas import StructuredQuery
from app.infrastructure.repositories.sqlite_repository import SQLiteRepository


class ShoppingWorkflow:
    """Shopping workflow using LangGraph."""
    
    def __init__(self):
        """Initialize the workflow."""
        self.graph = self._build_graph()
        self.app = self.graph.compile()
        self.repository = SQLiteRepository()  # Initialize repository
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow with iterative search support.
        
        Flow:
        1. check_conversation -> (if conversational) -> END
        2. check_conversation -> (else) -> check_feedback -> (if negative feedback + session) -> research_products -> compare_prices -> generate_message -> END
        3. check_conversation -> (else) -> check_feedback -> (else) -> understand_query -> research_products -> compare_prices -> generate_message -> END
        """
        workflow = StateGraph(ShoppingState)
        
        # Add nodes
        workflow.add_node("check_conversation", check_conversation_node)
        workflow.add_node("check_feedback", check_feedback_node)
        workflow.add_node("understand_query", understand_query_node)
        workflow.add_node("research_products", research_products_node)
        workflow.add_node("compare_prices", compare_prices_node)
        workflow.add_node("generate_message", generate_product_message_node)
        
        # Define conditional routing for conversation
        def is_conversational_route(state: ShoppingState) -> str:
            """Check if query is conversational."""
            if state.get("is_conversational", False):
                return "end"
            return "continue"
        
        # Define conditional routing for feedback
        def should_skip_understanding(state: ShoppingState) -> str:
            """
            Decide if we should skip understanding (reuse previous query).
            
            Returns:
                "skip" if negative feedback and session exists, "understand" otherwise
            """
            is_negative = state.get("is_negative_feedback", False)
            session_id = state.get("session_id")
            
            if is_negative and session_id:
                session = session_manager.get_session(session_id)
                if session and session.last_structured_query:
                    return "skip"
            
            return "understand"
        
        # Define edges
        workflow.set_entry_point("check_conversation")
        workflow.add_conditional_edges(
            "check_conversation",
            is_conversational_route,
            {
                "end": END,
                "continue": "check_feedback"
            }
        )
        workflow.add_conditional_edges(
            "check_feedback",
            should_skip_understanding,
            {
                "skip": "research_products",
                "understand": "understand_query"
            }
        )
        workflow.add_edge("understand_query", "research_products")
        workflow.add_edge("research_products", "compare_prices")
        workflow.add_edge("compare_prices", "generate_message")
        workflow.add_edge("generate_message", END)
        
        return workflow
    
    def run(self, user_message: str, session_id: Optional[str] = None) -> ShoppingState:
        """
        Execute the workflow.
        
        Args:
            user_message: User's message/query
            session_id: Optional session ID for iterative searches
            
        Returns:
            Final state with products and structured query
        """
        # Get or create session
        if not session_id:
            session_id = session_manager.create_session()
        else:
            # Ensure session exists
            if not session_manager.get_session(session_id):
                session_id = session_manager.create_session()
        
        # Get session data
        session = session_manager.get_session(session_id)
        excluded_links = session.excluded_product_links if session else []
        previous_query = session.last_structured_query if session else None
        
        # Ensure old StructuredQuery objects have new fields (backward compatibility)
        if previous_query and isinstance(previous_query, StructuredQuery):
            # Convert to dict and add missing fields
            if not hasattr(previous_query, 'condition') or previous_query.condition is None:
                previous_query_dict = previous_query.model_dump() if hasattr(previous_query, 'model_dump') else previous_query.dict()
                previous_query_dict.setdefault("condition", None)
                previous_query_dict.setdefault("style", None)
                try:
                    previous_query = StructuredQuery(**previous_query_dict)
                except:
                    # If conversion fails, set to None (will be regenerated)
                    previous_query = None
        
        # Initial state
        initial_state: ShoppingState = {
            "user_message": user_message,
            "session_id": session_id,
            "structured_query": previous_query,  # May be overridden by understand_query_node
            "products": [],
            "excluded_product_links": excluded_links,
            "price_comparison": None,
            "product_message": None,
            "is_conversational": False,
            "conversational_response": None,
            "is_negative_feedback": False,
            "error": None
        }
        
        # Run the workflow with error handling
        try:
            result = self.app.invoke(initial_state)
        except Exception as e:
            # If workflow fails, return error state
            import traceback
            print(f"Error in workflow execution: {str(e)}")
            print(traceback.format_exc())
            
            return {
                "user_message": user_message,
                "session_id": session_id,
                "structured_query": None,
                "products": [],
                "excluded_product_links": excluded_links,
                "price_comparison": None,
                "product_message": None,
                "is_conversational": False,
                "conversational_response": None,
                "is_negative_feedback": False,
                "error": f"Workflow error: {str(e)}"
            }
        
        # Update session with new data
        if result.get("structured_query"):
            try:
                session_manager.update_session(
                    session_id=session_id,
                    excluded_links=result.get("excluded_product_links", []),
                    structured_query=result.get("structured_query")
                )
            except Exception as e:
                # Don't fail if session update fails, just log it
                print(f"Warning: Failed to update session: {str(e)}")
        
        # Save to database
        try:
            # Save conversation
            assistant_response = result.get("conversational_response") or result.get("product_message")
            self.repository.save_conversation(
                session_id=session_id or "anonymous",
                user_message=user_message,
                assistant_response=assistant_response,
                structured_query=result.get("structured_query")
            )
            
            # Save search if products were found
            if result.get("products") and len(result.get("products", [])) > 0:
                query_text = result.get("structured_query").query_text if result.get("structured_query") else user_message
                self.repository.save_search(
                    session_id=session_id,
                    query_text=query_text,
                    structured_query=result.get("structured_query"),
                    num_results=len(result.get("products", []))
                )
                
                # Cache products
                self.repository.cache_products(
                    products=result.get("products", []),
                    search_query=query_text
                )
        except Exception as e:
            print(f"Warning: Failed to save to database: {str(e)}")
        
        return result

