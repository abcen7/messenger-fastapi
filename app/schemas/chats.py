from typing import Literal

from pydantic import BaseModel


class ChatCreate(BaseModel):
    title: str
    type: Literal["group", "private"]
    user_id_consumer: int
