from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreateSchema(BaseModel):
    conversation_id: int
    sender_id: int
    content: str

class MessageReadSchema(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str
    created_at: datetime
    read_at: Optional[datetime]