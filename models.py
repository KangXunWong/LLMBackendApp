from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
from uuid import UUID
from bson import ObjectId

class baseConversation(BaseModel):
    _id: ObjectId
    uuid: UUID
    id: str

class Conversation(BaseModel): 
    name: str
    params: Optional[dict] = {"additionalProp1": str}
    additionalProp1: Optional[dict] = Field(default=None)

class Message(BaseModel): 
    content: Optional[str] = Field(default=None)
    refusal: Optional[str] = Field(default=None)
    tool_calls: Optional[list] = Field(default=None)
    role: str

class Choices(BaseModel): 
    index: int
    message: Message
    logprobs: Optional[dict] = Field(default=None)
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
