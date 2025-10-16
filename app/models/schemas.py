from pydantic import BaseModel, Field
from typing import Optional, List, Any


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., min_length=1, description="User's message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Tell me more about Kiwi"
            }
        }


class ChatResponse(BaseModel):
    """Chat response schema"""
    response: str = Field(..., description="Chatbot's response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Kiwi is a nutrient-rich fruit priced at $2.49, rated 4.9 stars by our customers."
            }
        }


class Product(BaseModel):
    """Product schema"""
    id: int
    title: str
    description: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    brand: Optional[str] = None
    category: str
    thumbnail: str
    images: List[str]


class ProductsResponse(BaseModel):
    """Products list response schema"""
    products: List[Product]
    total: int
    skip: int
    limit: int


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "An error occurred while processing your request"
            }
        }
