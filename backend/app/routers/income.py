from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.income import IncomeCreate, IncomeResponse, IncomeUpdate
from app.services import income_service

router = APIRouter(prefix="/income", tags=["Income"])


@router.post("", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(
    income_data: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return income_service.create_income(db, current_user.id, income_data)


@router.get("", response_model=list[IncomeResponse])
def list_income(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return income_service.get_income_list(db, current_user.id)


@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(
    income_id: int,
    income_data: IncomeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return income_service.update_income(db, current_user.id, income_id, income_data)


@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    income_service.delete_income(db, current_user.id, income_id)
