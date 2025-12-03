from pydantic import BaseModel
from typing import List

class AIRequest(BaseModel):
    goal: str

class AIResponse(BaseModel):
    habits: List[str]

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str