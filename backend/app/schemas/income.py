from datetime import date as date_type
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class IncomeCreate(BaseModel):
    source: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    date: date_type


class IncomeUpdate(BaseModel):
    source: str | None = Field(None, min_length=1, max_length=100)
    amount: float | None = Field(None, gt=0)
    date: date_type | None = None


class IncomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    amount: float
    date: date_type
    created_at: datetime
    user_id: int
