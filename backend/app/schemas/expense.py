from datetime import date as date_type
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    description: str | None = None
    date: date_type


class ExpenseUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    amount: float | None = Field(None, gt=0)
    category: str | None = Field(None, min_length=1, max_length=50)
    description: str | None = None
    date: date_type | None = None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    amount: float
    category: str
    description: str | None
    date: date_type
    created_at: datetime
    user_id: int
