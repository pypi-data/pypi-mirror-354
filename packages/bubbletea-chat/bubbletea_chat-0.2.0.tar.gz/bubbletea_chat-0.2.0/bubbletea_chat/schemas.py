"""
Request and response schemas for BubbleTea
"""

from typing import List, Literal
from pydantic import BaseModel
from .components import Component


class ComponentChatRequest(BaseModel):
    """Incoming chat request from BubbleTea"""
    type: Literal["user"]
    message: str


class ComponentChatResponse(BaseModel):
    """Non-streaming response containing list of components"""
    responses: List[Component]