from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.dashboard import CategoryReportItem, IncomeVsExpenseItem, MonthlyReportItem
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly", response_model=list[MonthlyReportItem])
def monthly_report(
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.get_monthly_report(db, current_user.id, year)


@router.get("/category", response_model=list[CategoryReportItem])
def category_report(
    month: int | None = None,
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.get_category_report(db, current_user.id, month, year)


@router.get("/income-vs-expense", response_model=list[IncomeVsExpenseItem])
def income_vs_expense_report(
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.get_income_vs_expense_report(db, current_user.id, year)
