from pydantic import BaseModel, field_validator
from typing import Optional, List
from uuid import UUID

class baseConversation(BaseModel):
    uuid: UUID
    id: str

class Conversation(BaseModel): 
    name: str
    params: Optional[dict] = {"additionalProp1": str}
    additionalProp1: Optional[dict]

class Message(BaseModel): 
    content: Optional[str]
    refusal: Optional[str]
    tool_calls: Optional[list]
    role: str

class Choices(BaseModel): 
    index: int
    message: Message
    logprobs: Optional[dict]
    finish_reason: str

class Usage(BaseModel): 
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    completion_tokens_details: dict

class KastomQuery(BaseModel):
    role: str
    content: str
    additionalProp1: dict

class ChatCompletion(baseConversation, Conversation): 
    user_queries:List[KastomQuery]
    object: str
    created: int
    model: str
    system_fingerprint: str
    choices: List[Choices]
    usage: Usage
