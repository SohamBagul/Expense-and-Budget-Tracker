from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate


def create_income(db: Session, user_id: int, income_data: IncomeCreate) -> Income:
    income = Income(**income_data.model_dump(), user_id=user_id)
    db.add(income)
    db.commit()
    db.refresh(income)
    return income


def get_income_list(db: Session, user_id: int) -> list[Income]:
    return db.query(Income).filter(Income.user_id == user_id).order_by(Income.date.desc()).all()


def get_income(db: Session, user_id: int, income_id: int) -> Income:
    income = db.query(Income).filter(Income.id == income_id, Income.user_id == user_id).first()
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return income


def update_income(db: Session, user_id: int, income_id: int, income_data: IncomeUpdate) -> Income:
    income = get_income(db, user_id, income_id)
    update_data = income_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(income, field, value)
    db.commit()
    db.refresh(income)
    return income


def delete_income(db: Session, user_id: int, income_id: int) -> None:
    income = get_income(db, user_id, income_id)
    db.delete(income)
    db.commit()
