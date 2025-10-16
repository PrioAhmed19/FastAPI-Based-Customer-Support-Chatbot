from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    ChatRequest, 
    ChatResponse, 
    ProductsResponse, 
    ErrorResponse
)
from app.services.chatbot_service import chatbot_service
from app.services.product_service import product_service

router = APIRouter(prefix="/api", tags=["Chatbot"])


@router.get(
    "/products",
    response_model=ProductsResponse,
    summary="Get all products",
    description="Fetch all products from DummyJSON Products API"
)
async def get_products():
    """
    Retrieve all available products from the DummyJSON API.
    
    Returns:
        ProductsResponse: List of all products with metadata
    """
    try:
        products_data = await product_service.get_all_products()
        return products_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch products: {str(e)}"
        )


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        200: {
            "description": "Successful response",
            "model": ChatResponse
        },
        400: {
            "description": "Bad request",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    },
    summary="Chat with the product assistant",
    description="Send a message to the AI chatbot and get intelligent responses about products"
)
async def chat(request: ChatRequest):
    """
    Process a user message and return an AI-generated response about products.
    
    The chatbot can handle queries like:
    - "Tell me about Kiwi"
    - "What's the price of mango?"
    - "Show me electronics"
    - "Products with ratings above 4"
    
    Args:
        request: ChatRequest containing user's message
        
    Returns:
        ChatResponse: AI-generated response
    """
    try:
        if not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )
        
        response_text = await chatbot_service.process_message(request.message)
        
        return ChatResponse(response=response_text)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )
