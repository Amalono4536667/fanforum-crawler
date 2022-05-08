from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    author: str
    created_at: datetime
    votes: int
    quote: Optional[str]
    content: Optional[str]
    title: str
    signature: Optional[str]
