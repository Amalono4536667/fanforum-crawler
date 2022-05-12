from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Quote(BaseModel):
    author: str
    content: Optional[str]


class Comment(BaseModel):
    author: str
    created_at: datetime
    votes: int
    quote: Optional[Quote]
    content: Optional[str]
    title: str
    signature: Optional[str]
