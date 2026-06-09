"""OpenRouter AI Service Layer."""
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
from config.settings import settings
from core.exceptions import AIServiceError
from utils.logger import get_logger
from typing import Optional

logger = get_logger(__name__)


class OpenRouterService:
    """Service for interacting with OpenRouter API."""
    
    def __init__(self):
        """Initialize OpenRouter client."""
        if not settings.openrouter_api_key:
            raise AIServiceError(
                "OPENROUTER_API_KEY is not configured",
                "CONFIG_ERROR"
            )
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key
        )
        self.model = settings.model
        self.temperature = settings.temperature
        self.max_tokens = settings.max_tokens
        logger.info(f"OpenRouter service initialized with model: {self.model}")
    
    def chat(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Send a message to OpenRouter and get a response.
        
        Args:
            prompt: User message/prompt
            model: Override default model
            temperature: Override default temperature
            max_tokens: Override default max_tokens
        
        Returns:
            AI response text
        
        Raises:
            AIServiceError: If the API call fails
        """
        try:
            logger.info(f"Sending prompt to OpenRouter (model: {model or self.model})")
            
            completion = self.client.chat.completions.create(
                model=model or self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            
            response = completion.choices[0].message.content
            logger.info("Successfully received response from OpenRouter")
            return response
            
        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {str(e)}")
            raise AIServiceError(
                "API rate limit exceeded. Please try again later.",
                "RATE_LIMIT_ERROR"
            )
        except APIConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise AIServiceError(
                "Failed to connect to AI service. Please check your connection.",
                "CONNECTION_ERROR"
            )
        except APIError as e:
            logger.error(f"API error: {str(e)}")
            raise AIServiceError(
                f"AI service error: {str(e)}",
                "API_ERROR"
            )
        except Exception as e:
            logger.error(f"Unexpected error in OpenRouter service: {str(e)}")
            raise AIServiceError(
                f"Unexpected error: {str(e)}",
                "UNKNOWN_ERROR"
            )
