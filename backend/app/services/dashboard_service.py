from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.expense import Expense
from app.models.income import Income
from app.schemas.dashboard import (
    BudgetUsageItem,
    CategoryExpenseItem,
    DashboardSummary,
    DashboardSummaryExtended,
    MonthlyExpenseItem,
)
from app.utils.helpers import month_name, parse_month_year


def get_dashboard_summary(db: Session, user_id: int, month: int | None = None, year: int | None = None) -> DashboardSummaryExtended:
    month, year = parse_month_year(month, year)

    total_income = (
        db.query(func.coalesce(func.sum(Income.amount), 0.0))
        .filter(
            Income.user_id == user_id,
            extract("month", Income.date) == month,
            extract("year", Income.date) == year,
        )
        .scalar()
    )
    total_expense = (
        db.query(func.coalesce(func.sum(Expense.amount), 0.0))
        .filter(
            Expense.user_id == user_id,
            extract("month", Expense.date) == month,
            extract("year", Expense.date) == year,
        )
        .scalar()
    )

    budgets = (
        db.query(Budget)
        .filter(Budget.user_id == user_id, Budget.month == month, Budget.year == year)
        .all()
    )

    budget_usage: list[BudgetUsageItem] = []
    for budget in budgets:
        spent = (
            db.query(func.coalesce(func.sum(Expense.amount), 0.0))
            .filter(
                Expense.user_id == user_id,
                Expense.category == budget.category,
                extract("month", Expense.date) == month,
                extract("year", Expense.date) == year,
            )
            .scalar()
        )
        usage_percentage = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0.0
        budget_usage.append(
            BudgetUsageItem(
                category=budget.category,
                monthly_limit=budget.monthly_limit,
                spent=float(spent),
                usage_percentage=round(usage_percentage, 2),
            )
        )

    return DashboardSummaryExtended(
        total_income=float(total_income),
        total_expense=float(total_expense),
        remaining_balance=float(total_income) - float(total_expense),
        budget_usage=budget_usage,
    )


def get_category_wise_expenses(db: Session, user_id: int, month: int | None = None, year: int | None = None) -> list[CategoryExpenseItem]:
    month, year = parse_month_year(month, year)

    results = (
        db.query(Expense.category, func.sum(Expense.amount).label("total"))
        .filter(
            Expense.user_id == user_id,
            extract("month", Expense.date) == month,
            extract("year", Expense.date) == year,
        )
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )
    return [CategoryExpenseItem(category=r.category, total=float(r.total)) for r in results]


def get_monthly_expenses(db: Session, user_id: int, year: int | None = None) -> list[MonthlyExpenseItem]:
    year = year or parse_month_year(None, None)[1]

    results = (
        db.query(
            extract("month", Expense.date).label("month"),
            extract("year", Expense.date).label("year"),
            func.sum(Expense.amount).label("total"),
        )
        .filter(Expense.user_id == user_id, extract("year", Expense.date) == year)
        .group_by(extract("month", Expense.date), extract("year", Expense.date))
        .order_by(extract("month", Expense.date))
        .all()
    )
    return [
        MonthlyExpenseItem(
            month=month_name(int(r.month)),
            year=int(r.year),
            total=float(r.total),
        )
        for r in results
    ]
