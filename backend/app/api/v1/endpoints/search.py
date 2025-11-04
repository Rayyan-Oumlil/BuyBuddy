from fastapi import APIRouter, HTTPException
from app.models.schemas import SearchRequest, SearchResponse
from app.infrastructure.external_apis.serperdev_client import SerperDevClient

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    """
    Search products using SerperDev API.
    
    Example request:
    {
        "query": "laptop gaming under 1500 dollars"
    }
    """
    try:
        client = SerperDevClient()
        products = client.search_products(request.query, num_results=20)
        
        return SearchResponse(
            query=request.query,
            products=products,
            total=len(products)
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")

