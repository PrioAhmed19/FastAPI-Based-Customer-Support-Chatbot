from groq import Groq
from app.core.config import get_settings

settings = get_settings()


class GroqClient:
    """Groq API client for LLM interactions"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        
    async def generate_response(self, system_prompt: str, user_message: str) -> str:
        """
        Generate a response using Groq LLM
        
        Args:
            system_prompt: System instructions for the model
            user_message: User's input message
            
        Returns:
            Generated response text
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                model=self.model,
                temperature=settings.GROQ_TEMPERATURE,
                max_tokens=settings.GROQ_MAX_TOKENS,
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")


# Singleton instance
groq_client = GroqClient()
