from pydantic import BaseModel, field_validator, Field
from typing import Optional, List, Union
from uuid import UUID, uuid4
from bson import ObjectId

class baseConversation(BaseModel):
    _id: ObjectId
    uuid: UUID = uuid4()
    id: str

class Conversation(BaseModel):
    name: str =Field(max_length=200, title="Title of the conversation")
    params: Union[dict, None] = Field(default_factory=dict, description="Parameter dictionary for overriding defaults prescribed by the AI Model")
    user: str = Field(description="username of the user that started convo")

class Message(BaseModel):
    content: Optional[str] = Field(default=None)
    refusal: Optional[str] = Field(default=None)
    tool_calls: Union[list, None] = Field(default=None)
    role: str = Field(description="system role")

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
    role: str = Field(description="user role")
    content: str
    additionalProp1: Union[dict, None] = Field(default=None)

class ChatCompletion(baseConversation, Conversation):
    user_queries:List[KastomQuery]
    object: str
    created: int
    model: str
    system_fingerprint: str
    choices: List[Choices]
    usage: Usage

class FilesResponse(BaseModel):
    id: str
    object: str
    bytes: int
    created_at: int
    filename: str
    purpose: str = Field(enum=["assistants", "assistants_output", "batch", "batch_output", "fine-tune", "fine-tune-results", "vision"])