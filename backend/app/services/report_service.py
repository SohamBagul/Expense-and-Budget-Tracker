from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income
from app.schemas.dashboard import CategoryReportItem, IncomeVsExpenseItem, MonthlyReportItem
from app.utils.helpers import month_name, parse_month_year


def get_monthly_report(db: Session, user_id: int, year: int | None = None) -> list[MonthlyReportItem]:
    year = year or parse_month_year(None, None)[1]
    reports: list[MonthlyReportItem] = []

    for month in range(1, 13):
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
        income_val = float(total_income)
        expense_val = float(total_expense)
        reports.append(
            MonthlyReportItem(
                month=month,
                year=year,
                total_income=income_val,
                total_expense=expense_val,
                balance=income_val - expense_val,
            )
        )
    return reports


def get_category_report(db: Session, user_id: int, month: int | None = None, year: int | None = None) -> list[CategoryReportItem]:
    month, year = parse_month_year(month, year)

    total_expense = (
        db.query(func.coalesce(func.sum(Expense.amount), 0.0))
        .filter(
            Expense.user_id == user_id,
            extract("month", Expense.date) == month,
            extract("year", Expense.date) == year,
        )
        .scalar()
    )

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

    total = float(total_expense) if total_expense else 0.0
    return [
        CategoryReportItem(
            category=r.category,
            total_expense=float(r.total),
            percentage=round((float(r.total) / total * 100) if total > 0 else 0.0, 2),
        )
        for r in results
    ]


def get_income_vs_expense_report(db: Session, user_id: int, year: int | None = None) -> list[IncomeVsExpenseItem]:
    year = year or parse_month_year(None, None)[1]
    items: list[IncomeVsExpenseItem] = []

    for month in range(1, 13):
        income = (
            db.query(func.coalesce(func.sum(Income.amount), 0.0))
            .filter(
                Income.user_id == user_id,
                extract("month", Income.date) == month,
                extract("year", Income.date) == year,
            )
            .scalar()
        )
        expense = (
            db.query(func.coalesce(func.sum(Expense.amount), 0.0))
            .filter(
                Expense.user_id == user_id,
                extract("month", Expense.date) == month,
                extract("year", Expense.date) == year,
            )
            .scalar()
        )
        items.append(
            IncomeVsExpenseItem(
                month=month_name(month),
                year=year,
                income=float(income),
                expense=float(expense),
            )
        )
    return items
