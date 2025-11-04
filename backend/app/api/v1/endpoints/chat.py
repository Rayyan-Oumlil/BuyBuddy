"""
Chat endpoint for intelligent product search.
Uses LangGraph workflow to orchestrate agents.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.workflows.shopping_workflow import ShoppingWorkflow

router = APIRouter()

# Initialize workflow (singleton)
workflow = ShoppingWorkflow()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that understands user queries and searches for products.
    Uses LangGraph workflow to orchestrate the process.
    Supports iterative searches with session_id.
    
    Example request:
    {
        "message": "Je veux un laptop gaming sous 1500€",
        "session_id": "optional-session-id"
    }
    
    Returns structured query information and product results.
    """
    try:
        # Run the workflow with session_id
        result = workflow.run(request.message, session_id=request.session_id)
        
        # Get session_id from result
        session_id = result.get("session_id")
        
        # If there's an error, return it in the response instead of raising
        if result.get("error"):
            print(f"⚠️ Workflow error: {result.get('error')}")
            return ChatResponse(
                message=request.message,
                structured_query=result.get("structured_query"),
                products=result.get("products", []),
                session_id=session_id,
                price_comparison=None,
                conversational_response=None,
                product_message=None,
                error=result.get("error")
            )
        
        # Check if we have any response at all
        has_response = (
            result.get("conversational_response") or 
            result.get("products") or 
            result.get("product_message")
        )
        
        if not has_response:
            # If no response, create a fallback error message
            print(f"⚠️ No response generated for: {request.message}")
            return ChatResponse(
                message=request.message,
                structured_query=result.get("structured_query"),
                products=[],
                session_id=session_id,
                price_comparison=None,
                conversational_response=None,
                product_message=None,
                error="Aucune réponse générée. Veuillez réessayer."
            )
        
        # Build response
        response = ChatResponse(
            message=request.message,
            structured_query=result.get("structured_query"),
            products=result.get("products", []),
            session_id=session_id,
            price_comparison=result.get("price_comparison"),
            conversational_response=result.get("conversational_response"),
            product_message=result.get("product_message"),
            error=None
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        # Return error in response format instead of raising
        return ChatResponse(
            message=request.message,
            structured_query=None,
            products=[],
            session_id=request.session_id,
            price_comparison=None,
            conversational_response=None,
            product_message=None,
            error=f"Error processing chat: {str(e)}"
        )

