from typing import TypeVar

from pydantic import BaseModel

from app.models.base import Base

BaseORMModel = TypeVar("BaseORMModel", bound=Base)
DTO = TypeVar("DTO", bound=BaseModel)
