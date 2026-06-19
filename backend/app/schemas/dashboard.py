from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_income: float
    total_expense: float
    remaining_balance: float


class CategoryExpenseItem(BaseModel):
    category: str
    total: float


class MonthlyExpenseItem(BaseModel):
    month: str
    year: int
    total: float


class BudgetUsageItem(BaseModel):
    category: str
    monthly_limit: float
    spent: float
    usage_percentage: float


class DashboardSummaryExtended(DashboardSummary):
    budget_usage: list[BudgetUsageItem]


class MonthlyReportItem(BaseModel):
    month: int
    year: int
    total_income: float
    total_expense: float
    balance: float


class CategoryReportItem(BaseModel):
    category: str
    total_expense: float
    percentage: float


class IncomeVsExpenseItem(BaseModel):
    month: str
    year: int
    income: float
    expense: float
