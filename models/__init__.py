"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")


class HomeResponse(BaseModel):
    """Home endpoint response."""
    agent: str = Field(..., description="Agent name")
    status: str = Field(..., description="Agent status")
    model: str = Field(..., description="AI model in use")


class ChatRequest(BaseModel):
    """Chat request model."""
    prompt: str = Field(..., min_length=1, max_length=4096, description="User prompt")


class ChatResponse(BaseModel):
    """Generic AI response."""
    success: bool = Field(..., description="Whether the request succeeded")
    response: Optional[str] = Field(None, description="AI response")
    error: Optional[str] = Field(None, description="Error message if failed")


class ViralTitleRequest(BaseModel):
    """Viral title generation request."""
    topic: str = Field(..., min_length=1, max_length=500, description="Topic for title generation")


class ViralTitleResponse(BaseModel):
    """Viral title response."""
    success: bool = Field(..., description="Whether the request succeeded")
    topic: Optional[str] = Field(None, description="Topic provided")
    titles: Optional[str] = Field(None, description="Generated titles")
    error: Optional[str] = Field(None, description="Error message if failed")


class ThumbnailRequest(BaseModel):
    """Thumbnail idea request."""
    topic: str = Field(..., min_length=1, max_length=500, description="Topic for thumbnail ideas")


class ThumbnailResponse(BaseModel):
    """Thumbnail ideas response."""
    success: bool = Field(..., description="Whether the request succeeded")
    topic: Optional[str] = Field(None, description="Topic provided")
    thumbnail_ideas: Optional[str] = Field(None, description="Generated thumbnail ideas")
    error: Optional[str] = Field(None, description="Error message if failed")


class ContentStrategyRequest(BaseModel):
    """Content strategy request."""
    niche: str = Field(..., min_length=1, max_length=500, description="YouTube niche for strategy")


class ContentStrategyResponse(BaseModel):
    """Content strategy response."""
    success: bool = Field(..., description="Whether the request succeeded")
    niche: Optional[str] = Field(None, description="Niche provided")
    strategy: Optional[str] = Field(None, description="Generated strategy")
    error: Optional[str] = Field(None, description="Error message if failed")
