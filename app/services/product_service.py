import httpx
from typing import Dict, List, Optional
from app.core.config import get_settings

settings = get_settings()


class ProductService:
    """Service for interacting with DummyJSON Products API"""
    
    def __init__(self):
        self.base_url = settings.DUMMYJSON_BASE_URL
        
    async def get_all_products(self) -> Dict:
        """
        Fetch all products from DummyJSON API
        
        Returns:
            Dictionary containing products data
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/products?limit=0")
            response.raise_for_status()
            return response.json()
    
    async def search_products(self, query: str) -> List[Dict]:
        """
        Search products by query
        
        Args:
            query: Search query string
            
        Returns:
            List of matching products
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/products/search",
                params={"q": query}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("products", [])
    
    async def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """
        Get a single product by ID
        
        Args:
            product_id: Product ID
            
        Returns:
            Product data or None
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/products/{product_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None
    
    async def get_products_by_category(self, category: str) -> List[Dict]:
        """
        Get products by category
        
        Args:
            category: Product category
            
        Returns:
            List of products in the category
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/products/category/{category}"
            )
            response.raise_for_status()
            data = response.json()
            return data.get("products", [])
    
    async def filter_products_by_rating(self, min_rating: float) -> List[Dict]:
        """
        Filter products by minimum rating
        
        Args:
            min_rating: Minimum rating threshold
            
        Returns:
            List of products with rating >= min_rating
        """
        all_products_data = await self.get_all_products()
        products = all_products_data.get("products", [])
        return [p for p in products if p.get("rating", 0) >= min_rating]


# Singleton instance
product_service = ProductService()
