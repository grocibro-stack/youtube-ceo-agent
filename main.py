"""
YouTube CEO Agent FastAPI Application.

Production-ready API for YouTube content generation using OpenRouter AI.
"""
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from typing import Optional
from contextlib import asynccontextmanager

# Import configuration, services, and models
from config.settings import settings
from services.openrouter_service import OpenRouterService
from services.error_handler import handle_service_error, global_exception_handler
from core.exceptions import AIServiceError, ValidationError
from utils.logger import get_logger
from models import (
    HomeResponse,
    HealthResponse,
    ChatRequest,
    ChatResponse,
    ViralTitleRequest,
    ViralTitleResponse,
    ThumbnailRequest,
    ThumbnailResponse,
    ContentStrategyRequest,
    ContentStrategyResponse,
)

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger(__name__)

# Global AI service instance
ai_service: Optional[OpenRouterService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Initializes resources on startup and cleans up on shutdown.
    """
    global ai_service
    
    # Startup
    logger.info("Starting YouTube CEO Agent API...")
    try:
        ai_service = OpenRouterService()
        logger.info("✓ AI service initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize AI service: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down YouTube CEO Agent API...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="YouTube CEO Agent API",
    version="2.0",
    description="AI-powered YouTube content generation and strategy planning",
    lifespan=lifespan,
)

# Register global exception handler
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/", response_model=HomeResponse, tags=["System"])
def home() -> HomeResponse:
    """
    Home endpoint - returns API information.
    
    **EXPLANATION:**
    - Returns basic API metadata
    - Confirms API is running
    - Shows active AI model
    """
    logger.info("GET / - Home endpoint called")
    
    return HomeResponse(
        agent="YouTube CEO Agent",
        status="running",
        model=settings.model
    )


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health() -> HealthResponse:
    """
    Health check endpoint - confirms API is healthy.
    
    **EXPLANATION:**
    - Used for monitoring and load balancer health checks
    - Always returns 200 OK if service is up
    """
    logger.info("GET /health - Health check called")
    
    return HealthResponse(status="healthy")


@app.post("/chat", response_model=ChatResponse, tags=["AI"])
def chat(request: ChatRequest) -> ChatResponse:
    """
    Generic chat endpoint - send any prompt to AI.
    
    **EXPLANATION:**
    - Accepts a user prompt
    - Sends to OpenRouter AI
    - Returns AI response
    - Includes comprehensive error handling
    
    Args:
        request: ChatRequest with prompt field
    
    Returns:
        ChatResponse with success flag and response or error
    """
    logger.info(f"POST /chat - Prompt length: {len(request.prompt)} chars")
    
    try:
        if not request.prompt.strip():
            logger.warning("Empty prompt provided")
            return ChatResponse(
                success=False,
                error="Prompt cannot be empty"
            )
        
        logger.debug(f"Processing prompt: {request.prompt[:100]}...")
        answer = ai_service.chat(request.prompt)
        
        logger.info("Chat request completed successfully")
        return ChatResponse(
            success=True,
            response=answer
        )
    
    except AIServiceError as e:
        logger.error(f"AI service error in /chat: {e.message}")
        return ChatResponse(
            success=False,
            error=e.message
        )
    except Exception as e:
        logger.error(f"Unexpected error in /chat: {str(e)}", exc_info=True)
        return ChatResponse(
            success=False,
            error="An unexpected error occurred"
        )


@app.post("/viral-title", response_model=ViralTitleResponse, tags=["YouTube"])
def viral_title(request: ViralTitleRequest) -> ViralTitleResponse:
    """
    Generate viral YouTube titles for a topic.
    
    **EXPLANATION:**
    - Takes a YouTube topic
    - Generates 10 CTR-optimized titles
    - Uses AI to understand viral patterns
    - Returns structured title suggestions
    
    Args:
        request: ViralTitleRequest with topic field
    
    Returns:
        ViralTitleResponse with generated titles or error
    """
    logger.info(f"POST /viral-title - Topic: {request.topic}")
    
    try:
        if not request.topic.strip():
            logger.warning("Empty topic provided")
            return ViralTitleResponse(
                success=False,
                error="Topic cannot be empty"
            )
        
        prompt = f"""
Generate 10 viral YouTube titles about:

{request.topic}

Requirements:
- High CTR (Click-Through Rate)
- Curiosity driven
- Modern YouTube style
- Numbered list format (1. Title, 2. Title, etc.)
- Each title 40-60 characters max
"""

        logger.debug(f"Sending title generation prompt for topic: {request.topic}")
        answer = ai_service.chat(prompt)
        
        logger.info("Viral title generation completed successfully")
        return ViralTitleResponse(
            success=True,
            topic=request.topic,
            titles=answer
        )
    
    except AIServiceError as e:
        logger.error(f"AI service error in /viral-title: {e.message}")
        return ViralTitleResponse(
            success=False,
            error=e.message
        )
    except Exception as e:
        logger.error(f"Unexpected error in /viral-title: {str(e)}", exc_info=True)
        return ViralTitleResponse(
            success=False,
            error="Failed to generate titles"
        )


@app.post("/thumbnail", response_model=ThumbnailResponse, tags=["YouTube"])
def thumbnail(request: ThumbnailRequest) -> ThumbnailResponse:
    """
    Generate YouTube thumbnail design ideas.
    
    **EXPLANATION:**
    - Takes a video topic
    - Generates 5 thumbnail design concepts
    - Includes visual elements and emotions
    - Helps creators design high-performing thumbnails
    
    Args:
        request: ThumbnailRequest with topic field
    
    Returns:
        ThumbnailResponse with thumbnail ideas or error
    """
    logger.info(f"POST /thumbnail - Topic: {request.topic}")
    
    try:
        if not request.topic.strip():
            logger.warning("Empty topic provided for thumbnails")
            return ThumbnailResponse(
                success=False,
                error="Topic cannot be empty"
            )
        
        prompt = f"""
Generate 5 YouTube thumbnail design ideas for:

{request.topic}

For each idea include:
- Thumbnail text (max 3 words)
- Dominant emotion (excited, shocked, curious, etc.)
- Visual concept (what elements to include)
- Color scheme (primary 2 colors)
- Target reaction (what viewers will feel)

Format as a numbered list.
"""

        logger.debug(f"Sending thumbnail generation prompt for topic: {request.topic}")
        answer = ai_service.chat(prompt)
        
        logger.info("Thumbnail generation completed successfully")
        return ThumbnailResponse(
            success=True,
            topic=request.topic,
            thumbnail_ideas=answer
        )
    
    except AIServiceError as e:
        logger.error(f"AI service error in /thumbnail: {e.message}")
        return ThumbnailResponse(
            success=False,
            error=e.message
        )
    except Exception as e:
        logger.error(f"Unexpected error in /thumbnail: {str(e)}", exc_info=True)
        return ThumbnailResponse(
            success=False,
            error="Failed to generate thumbnail ideas"
        )


@app.post("/content-strategy", response_model=ContentStrategyResponse, tags=["YouTube"])
def content_strategy(request: ContentStrategyRequest) -> ContentStrategyResponse:
    """
    Generate complete YouTube content strategy.
    
    **EXPLANATION:**
    - Takes a YouTube niche
    - Generates comprehensive strategy
    - Includes audience analysis, topics, posting frequency, monetization
    - Provides growth roadmap for channel scaling
    
    Args:
        request: ContentStrategyRequest with niche field
    
    Returns:
        ContentStrategyResponse with strategy or error
    """
    logger.info(f"POST /content-strategy - Niche: {request.niche}")
    
    try:
        if not request.niche.strip():
            logger.warning("Empty niche provided")
            return ContentStrategyResponse(
                success=False,
                error="Niche cannot be empty"
            )
        
        prompt = f"""
Create a complete YouTube content strategy for the niche:

{request.niche}

Include detailed sections for:
1. Target Audience Analysis
   - Demographics
   - Pain points
   - What they watch

2. Viral Topic Ideas
   - 15-20 trending topics
   - Why each will perform well

3. Content Pillars
   - 3-5 main content categories

4. Posting Frequency
   - Recommended schedule
   - Best upload times

5. SEO & Discoverability
   - Keyword strategy
   - Tag recommendations

6. Monetization Strategy
   - When to enable monetization
   - Revenue streams

7. Growth Roadmap
   - 30-day milestones
   - 90-day milestones
   - 6-month goals
"""

        logger.debug(f"Sending strategy generation prompt for niche: {request.niche}")
        answer = ai_service.chat(prompt)
        
        logger.info("Content strategy generation completed successfully")
        return ContentStrategyResponse(
            success=True,
            niche=request.niche,
            strategy=answer
        )
    
    except AIServiceError as e:
        logger.error(f"AI service error in /content-strategy: {e.message}")
        return ContentStrategyResponse(
            success=False,
            error=e.message
        )
    except Exception as e:
        logger.error(f"Unexpected error in /content-strategy: {str(e)}", exc_info=True)
        return ContentStrategyResponse(
            success=False,
            error="Failed to generate content strategy"
        )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )