from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class FunctionCall(BaseModel):
    arguments: str
    name: str


class Content(BaseModel):
    type: str
    text: str

class ContentThinking(BaseModel):
    type: str
    text: str
    signature: Optional[str] = None

class ContentRedactedThinking(BaseModel):
    type: str
    data: str

class ToolCall(BaseModel):
    index: int = Field(default=None)
    function: FunctionCall
    id: str
    type: str = "function"

class ThinkingBlock(BaseModel):
    type: str 
    thinking: str 
    signature: Optional[str] = None
    data: Optional[str] = None

class Message(BaseModel):
    role: str
    agent_name: str
    content: Optional[List[Content|ContentThinking|ContentRedactedThinking]] = Field(default_factory=list)
    tool_calls: Optional[List[dict]] = None
    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None
    hidden: bool = False
    id: Optional[str] = None
    usage: Optional[Usage] = None
    type: Optional[str] = None

    def to_oai_style(self) -> Dict[str, str]:
        """Returns a dictionary containing only 'role' and 'content'"""
        return {
            "role": self.role,
            "content": self.content
        }

    model_config = {
        "exclude_none": True
    }


class Response(BaseModel):
    call_id: str
    agent_name: str
    role: str
    content: str 
    tool_calls: List[ToolCall] = Field(default_factory=list)
    thinking_blocks: List[ThinkingBlock] = Field(default_factory=list)
    usage: Optional[Usage] = Field(default=None)
    reasoning_content: Optional[str] = Field(default=None)

    model_config = {
        "exclude_none": True
    }


class StreamResponse(BaseModel):
    call_id: str
    agent_name: str
    role: str
    content: Optional[str] = None
    reasoning_content: Optional[str] = None
    is_thinking: bool = False
    is_tool_call: bool = False
    tool_name: Optional[str] = None
    is_tool_exec: bool = False
    tool_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    usage: Optional[Usage] = Field(default=None)
    thinking_blocks: Optional[List[ThinkingBlock]] = Field(default=None)
    model_config = {
        "exclude_none": True
    }


class ConversationHistory(BaseModel):
    messages: List[Message] = Field(default_factory=list)

