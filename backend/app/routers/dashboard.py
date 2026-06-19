from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.dashboard import CategoryExpenseItem, DashboardSummaryExtended, MonthlyExpenseItem
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryExtended)
def get_summary(
    month: int | None = None,
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return dashboard_service.get_dashboard_summary(db, current_user.id, month, year)


@router.get("/category-wise", response_model=list[CategoryExpenseItem])
def get_category_wise(
    month: int | None = None,
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return dashboard_service.get_category_wise_expenses(db, current_user.id, month, year)


@router.get("/monthly", response_model=list[MonthlyExpenseItem])
def get_monthly(
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return dashboard_service.get_monthly_expenses(db, current_user.id, year)
