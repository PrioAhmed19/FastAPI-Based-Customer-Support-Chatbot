import json
import re
from typing import Dict, List, Optional
from app.services.product_service import product_service
from app.utils.groq_client import groq_client


class ChatbotService:
    """Service for handling chatbot logic and responses"""
    
    def __init__(self):
        self.product_service = product_service
        self.groq_client = groq_client
        
    async def process_message(self, user_message: str) -> str:
        """
        Process user message and generate appropriate response
        
        Args:
            user_message: User's input message
            
        Returns:
            Chatbot response
        """
        # Step 1: Analyze intent and extract entities
        intent_data = await self._analyze_intent(user_message)
        
        # Step 2: Fetch relevant product data
        product_context = await self._fetch_product_context(intent_data, user_message)
        
        # Step 3: Generate natural language response
        response = await self._generate_response(user_message, product_context)
        
        return response
    
    async def _analyze_intent(self, message: str) -> Dict:
        """
        Analyze user intent using Groq LLM
        
        Args:
            message: User's message
            
        Returns:
            Dictionary containing intent and entities
        """
        system_prompt = """You are an intent classifier for a product inquiry chatbot. 
Analyze the user's message and extract:
1. intent: The type of query (product_info, price_inquiry, rating_inquiry, category_search, general_inquiry)
2. product_name: The product mentioned (if any)
3. category: Product category mentioned (if any)
4. rating_threshold: Minimum rating if user asks for highly rated products (if any)

Respond ONLY with a valid JSON object. Example:
{"intent": "product_info", "product_name": "kiwi", "category": null, "rating_threshold": null}
"""
        
        response = await self.groq_client.generate_response(system_prompt, message)
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"intent": "general_inquiry", "product_name": None, "category": None, "rating_threshold": None}
        except:
            return {"intent": "general_inquiry", "product_name": None, "category": None, "rating_threshold": None}
    
    async def _fetch_product_context(self, intent_data: Dict, original_message: str) -> str:
        """
        Fetch relevant product data based on intent
        
        Args:
            intent_data: Extracted intent and entities
            original_message: Original user message
            
        Returns:
            Product context as formatted string
        """
        try:
            intent = intent_data.get("intent")
            product_name = intent_data.get("product_name")
            category = intent_data.get("category")
            rating_threshold = intent_data.get("rating_threshold")
            
            products = []
            
            # Handle different intents
            if product_name:
                # Search for specific product
                products = await self.product_service.search_products(product_name)
            elif category:
                # Search by category
                products = await self.product_service.get_products_by_category(category)
            elif rating_threshold:
                # Filter by rating
                products = await self.product_service.filter_products_by_rating(float(rating_threshold))
            else:
                # General inquiry - get some popular products
                all_data = await self.product_service.get_all_products()
                products = all_data.get("products", [])[:5]
            
            if not products:
                return "No products found matching your query."
            
            # Format product data for LLM context
            return self._format_products_for_context(products[:5])  # Limit to 5 products
            
        except Exception as e:
            return f"Error fetching product data: {str(e)}"
    
    def _format_products_for_context(self, products: List[Dict]) -> str:
        """
        Format product data into readable context for LLM
        
        Args:
            products: List of product dictionaries
            
        Returns:
            Formatted product information string
        """
        if not products:
            return "No products available."
        
        context_parts = []
        for product in products:
            context_parts.append(f"""
Product: {product.get('title', 'Unknown')}
Description: {product.get('description', 'No description')}
Price: ${product.get('price', 0)}
Discount: {product.get('discountPercentage', 0)}%
Rating: {product.get('rating', 0)}/5
Stock: {product.get('stock', 0)} units
Brand: {product.get('brand', 'N/A')}
Category: {product.get('category', 'N/A')}
""")
        
        return "\n---\n".join(context_parts)
    
    async def _generate_response(self, user_message: str, product_context: str) -> str:
        """
        Generate natural language response using Groq LLM
        
        Args:
            user_message: User's original message
            product_context: Retrieved product information
            
        Returns:
            Natural language response
        """
        system_prompt = f"""You are a friendly and knowledgeable product specialist chatbot. 
Your job is to help customers learn about products in a natural, conversational way.

Guidelines:
- Be helpful, friendly, and concise
- Use the product information provided to answer questions accurately
- If multiple products match, mention the most relevant ones
- Include key details like price, rating, and availability when relevant
- If no relevant products are found, politely suggest alternatives or ask for clarification
- Don't make up information - only use the data provided
- Keep responses conversational and natural, not robotic

Available Product Information:
{product_context}
"""
        
        response = await self.groq_client.generate_response(system_prompt, user_message)
        return response


# Singleton instance
chatbot_service = ChatbotService()
