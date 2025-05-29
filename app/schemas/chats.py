from typing import Literal

from pydantic import BaseModel


class CreateChat(BaseModel):
    title: str
    type: Literal["group", "private"]
