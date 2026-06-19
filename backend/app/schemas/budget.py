from pydantic import BaseModel, ConfigDict, Field


class BudgetCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=50)
    monthly_limit: float = Field(..., gt=0)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2100)


class BudgetUpdate(BaseModel):
    category: str | None = Field(None, min_length=1, max_length=50)
    monthly_limit: float | None = Field(None, gt=0)
    month: int | None = Field(None, ge=1, le=12)
    year: int | None = Field(None, ge=2000, le=2100)


class BudgetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    monthly_limit: float
    month: int
    year: int
    user_id: int
