from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
import json


class CacheEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    input_hash: str = Field(index=True)
    transformed_data: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PayloadRequest(SQLModel):
    list_1: List[str]
    list_2: List[str]


class PayloadResponse(SQLModel):
    output: str
